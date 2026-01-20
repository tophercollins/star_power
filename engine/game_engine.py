from typing import List, Dict, Any, Tuple, Optional
from engine.serializers import player_view, deck_view, event_view
from engine.rules.common_ops import play_card_from_hand
from engine.rules.event_ops import draw_event, resolve_event, award_fans, remove_fans, count_player_fans
from engine.rules.deck_ops import draw_card
# from engine.rules.power_ops import attach_power_by_ids
from engine.models.cards import StarCard, PowerCard
from engine.ai import ComputerPlayer
from resources.config import GAME_CONFIG
import logging

logger = logging.getLogger(__name__)

class GameEngine:
    def __init__(self, players: List[Any], decks: Tuple[Any, Any, Any]):
        logger.info("Initializing GameEngine")
        self.players = players
        self.main_deck, self.event_deck, self.fan_deck = decks
        self.turn = 1
        self.phase = "play"  # "play", "event_select", "event_resolve", "game_over"

        # Event state
        self.current_event: Optional[Any] = None
        self.player_selections: Dict[int, Dict[str, Any]] = {}  # {player_index: {star, stat}}

        # Turn-based play tracking
        self.stars_played_this_turn: Dict[int, int] = {0: 0, 1: 0}  # {player_index: count}
        self.powers_played_this_turn: Dict[int, int] = {0: 0, 1: 0}  # {player_index: count}

        # Turn order rotation - tracks which player goes first each turn
        self.first_player_index: int = 0  # Alternates each turn

        # Legacy pending card (for power cards)
        self.pending_card: Optional[Dict[str, Any]] = None

        # Computer AI
        self.computer_ai = ComputerPlayer(player_index=1)

        # Game ending state
        self.winner: Optional[int] = None
        self.game_over_reason: Optional[str] = None

    def dispatch(self, command: dict) -> Dict[str, Any]:
        action = command.get("type")
        payload = command.get("payload", {})
        logger.info(f"Dispatch: {action} {payload}")

        if action == "PLAY_CARD":
            player_index = payload.get("player", 0)
            hand_index = payload.get("hand_index")
            target_star_index = payload.get("target_star_index")  # For power cards

            if 0 <= player_index < len(self.players):
                player = self.players[player_index]

                # Validate hand_index and get the card
                if hand_index is None or hand_index < 0 or hand_index >= len(player.hand):
                    logger.warning(f"Invalid hand index {hand_index} for player {player.name}")
                    return self.snapshot()

                card = player.hand[hand_index]

                # Check turn limits based on card type
                from engine.models.cards import StarCard, PowerCard
                if isinstance(card, StarCard):
                    if self.stars_played_this_turn[player_index] >= 1:
                        logger.warning(f"Player {player.name} already played a star this turn")
                        return self.snapshot()
                elif isinstance(card, PowerCard):
                    if self.powers_played_this_turn[player_index] >= 1:
                        logger.warning(f"Player {player.name} already played a power card this turn")
                        return self.snapshot()

                # Delegate to common_ops which handles all card types
                play_card_from_hand(player, hand_index, target_star_index=target_star_index)

                # Track the play
                if isinstance(card, StarCard):
                    self.stars_played_this_turn[player_index] += 1
                elif isinstance(card, PowerCard):
                    self.powers_played_this_turn[player_index] += 1
            else:
                logger.warning(f"Invalid player index: {player_index}")

        elif action == "END_TURN":
            self._handle_end_turn()

        elif action == "SELECT_STAR_FOR_EVENT":
            player_index = payload.get("player", 0)
            star_index = payload.get("star_index")
            chosen_stat = payload.get("stat")

            if 0 <= player_index < len(self.players):
                player = self.players[player_index]

                # Validate star selection
                if star_index is not None and 0 <= star_index < len(player.star_cards):
                    star = player.star_cards[star_index]
                    self.player_selections[player_index] = {
                        "star": star,
                        "stat": chosen_stat
                    }
                    logger.info(f"Player {player_index} selected {star.name} with stat {chosen_stat} for event")
                    # Note: Event will resolve when both players have selected (triggered by End Turn)
                else:
                    logger.warning(f"Invalid star index: {star_index}")
            else:
                logger.warning(f"Invalid player index: {player_index}")

        elif action == "RESOLVE_EVENT":
            # Manual event resolution trigger
            self._resolve_current_event()

        return self.snapshot()

    def _handle_end_turn(self):
        """Handle end of turn - computer plays, selects star, event resolves

        Flow:
        - Turn 1: Computer plays → Advance to turn 2 (draw event for turn 2)
        - Turn 2+: Player selects star (already done) → Computer plays + selects star → Event resolves → Advance to next turn

        Star selection is part of each player's turn, done during play phase.
        """
        logger.info(f"Ending turn {self.turn}")

        # Computer AI takes its turn (seeing current event if it exists)
        logger.info("Computer AI taking turn...")
        self.computer_ai.take_turn(self)

        # If there's an active event, computer selects for it (as last part of their turn)
        if self.current_event:
            self._computer_select_for_event()
            # Both players should have selected by now, resolve event
            if len(self.player_selections) == 2:
                self._resolve_current_event()
            else:
                logger.warning(f"Event exists but not all players selected (selections: {len(self.player_selections)})")
                # Resolve anyway with whoever selected
                self._resolve_current_event()
        else:
            # Turn 1: No event yet, just advance to next turn
            self._advance_to_next_turn()

    def _resolve_current_event(self):
        """Resolve the current event with player selections

        Exhaustion flow:
        1. FIRST: Refresh all currently exhausted stars
        2. THEN: Resolve event with selected stars
        3. THEN: Mark participating stars as exhausted
        """
        if not self.current_event:
            logger.warning("No active event to resolve")
            return

        # STEP 1: Reset exhaustion for all stars BEFORE event resolution
        # This happens at the start of the event phase, after all players have taken their turns
        logger.info("Refreshing exhausted stars before event resolution...")
        for player in self.players:
            for star in player.star_cards:
                if star.exhausted:
                    star.exhausted = False
                    logger.info(f"{star.name} is no longer exhausted")

        # Get player selections
        p1_selection = self.player_selections.get(0, {})
        p2_selection = self.player_selections.get(1, {})

        p1_star = p1_selection.get("star")
        p1_stat = p1_selection.get("stat")
        p2_star = p2_selection.get("star")
        p2_stat = p2_selection.get("stat")

        # STEP 2: Resolve the event
        result = resolve_event(
            self.current_event,
            p1_star, p2_star,
            p1_stat, p2_stat,
            self.fan_deck
        )

        # Award/remove fans based on result
        if result["player1_fans_won"] > 0:
            fans = award_fans(self.players[0], self.fan_deck, result["player1_fans_won"])
            # Attach to the star that competed
            if p1_star and fans:
                p1_star.attached_fans.extend(fans)

        if result["player2_fans_won"] > 0:
            fans = award_fans(self.players[1], self.fan_deck, result["player2_fans_won"])
            if p2_star and fans:
                p2_star.attached_fans.extend(fans)

        if result["player1_fans_lost"] > 0:
            remove_fans(self.players[0], result["player1_fans_lost"])

        if result["player2_fans_lost"] > 0:
            remove_fans(self.players[1], result["player2_fans_lost"])

        logger.info(f"Event resolved: {result['description']}")

        # STEP 3: Mark participating stars as exhausted
        # (This happens in resolve_event in event_ops.py)

        # Check for game over
        self._check_win_condition()

        # Clear event state
        self.current_event = None
        self.player_selections = {}

        # Set phase based on game state
        if self.phase == "game_over":
            return  # Keep game_over phase
        else:
            # Advance to next turn
            self._advance_to_next_turn()

    def _check_win_condition(self):
        """Check if any player has reached the win condition"""
        fans_to_win = GAME_CONFIG["fans_to_win"]

        player1_fans = count_player_fans(self.players[0])
        player2_fans = count_player_fans(self.players[1])

        if player1_fans >= fans_to_win:
            self.winner = 0
            self.phase = "game_over"
            self.game_over_reason = f"{self.players[0].name} wins with {player1_fans} fans!"
            logger.info(f"GAME OVER: {self.game_over_reason}")
        elif player2_fans >= fans_to_win:
            self.winner = 1
            self.phase = "game_over"
            self.game_over_reason = f"{self.players[1].name} wins with {player2_fans} fans!"
            logger.info(f"GAME OVER: {self.game_over_reason}")

    def _advance_to_next_turn(self):
        """Advance to next turn - draw cards, increment turn, draw next event

        This happens AFTER event resolution, preparing for the next turn.
        """
        # Draw cards for both players
        for i, player in enumerate(self.players):
            card = draw_card(self.main_deck)
            if card:
                player.hand.append(card)
                logger.info(f"{player.name} drew a card: {card.name}")

        # Increment turn
        self.turn += 1
        logger.info(f"Turn {self.turn} started")

        # Rotate first player (alternates each turn)
        self.first_player_index = (self.first_player_index + 1) % len(self.players)
        logger.info(f"First player this turn: {self.players[self.first_player_index].name}")

        # Reset play counters
        self.stars_played_this_turn = {0: 0, 1: 0}
        self.powers_played_this_turn = {0: 0, 1: 0}

        # Draw NEXT event if turn >= 2 (so it's visible when turn starts)
        if self.turn >= 2 and len(self.event_deck.cards) > 0:
            # Draw the event for this turn
            self.current_event = draw_event(self.event_deck)
            logger.info(f"Event drawn for turn {self.turn}: {self.current_event.name}")

        # Set phase to play
        self.phase = "play"

    def _computer_select_for_event(self):
        """Have computer AI automatically select for event"""
        if not self.current_event:
            return

        selection = self.computer_ai.select_for_event(self, self.current_event)
        if selection:
            star_index = selection["star_index"]
            stat = selection["stat"]

            # Make the selection
            player = self.players[1]
            if 0 <= star_index < len(player.star_cards):
                star = player.star_cards[star_index]
                self.player_selections[1] = {
                    "star": star,
                    "stat": stat
                }
                logger.info(f"Computer selected {star.name} with stat {stat}")

                # Auto-resolve if both players have selected (won't happen yet since player hasn't selected)
                if len(self.player_selections) == 2:
                    self._resolve_current_event()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "turn": self.turn,
            "phase": self.phase,
            "first_player_index": self.first_player_index,
            "current_event": event_view(self.current_event),
            "player_selections": {
                str(k): {"star_id": v["star"].id if "star" in v else None, "stat": v.get("stat")}
                for k, v in self.player_selections.items()
            },
            "players": [player_view(player, player_index=i) for i, player in enumerate(self.players)],
            "main_deck": deck_view(self.main_deck),
            "event_deck": deck_view(self.event_deck),
            "fan_deck": deck_view(self.fan_deck),
            "fan_counts": {
                "player1": count_player_fans(self.players[0]),
                "player2": count_player_fans(self.players[1])
            },
            "game_over": self.phase == "game_over",
            "winner": self.winner,
            "game_over_reason": self.game_over_reason,
            "fans_to_win": GAME_CONFIG["fans_to_win"]
        }

    