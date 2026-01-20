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
                    logger.info(f"Player {player_index} selected {star.name} with stat {chosen_stat}")

                    # Auto-resolve if both players have selected
                    if len(self.player_selections) == 2:
                        self._resolve_current_event()
                else:
                    logger.warning(f"Invalid star index: {star_index}")
            else:
                logger.warning(f"Invalid player index: {player_index}")

        elif action == "RESOLVE_EVENT":
            # Manual event resolution trigger
            self._resolve_current_event()

        return self.snapshot()

    def _handle_end_turn(self):
        """Handle end of turn - draw cards, trigger event if applicable, let computer play"""
        logger.info(f"Ending turn {self.turn}")

        # Draw card for each player
        for i, player in enumerate(self.players):
            card = draw_card(self.main_deck)
            if card:
                player.hand.append(card)
                logger.info(f"{player.name} drew a card: {card.name}")

        # Increment turn and reset play counters
        self.turn += 1
        self.stars_played_this_turn = {0: 0, 1: 0}
        self.powers_played_this_turn = {0: 0, 1: 0}
        logger.info(f"Turn {self.turn} started - play counters reset")

        # Computer AI takes its turn
        logger.info("Computer AI taking turn...")
        self.computer_ai.take_turn(self)

        # Trigger event starting from turn 2
        if self.turn >= 2 and len(self.event_deck.cards) > 0:
            self.current_event = draw_event(self.event_deck)
            self.phase = "event_select"
            self.player_selections = {}
            logger.info(f"Event triggered: {self.current_event.name}")

            # Computer AI auto-selects for event
            self._computer_select_for_event()
        else:
            self.phase = "play"

    def _resolve_current_event(self):
        """Resolve the current event with player selections"""
        if not self.current_event:
            logger.warning("No active event to resolve")
            return

        # Get player selections
        p1_selection = self.player_selections.get(0, {})
        p2_selection = self.player_selections.get(1, {})

        p1_star = p1_selection.get("star")
        p1_stat = p1_selection.get("stat")
        p2_star = p2_selection.get("star")
        p2_stat = p2_selection.get("stat")

        # Resolve the event
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

        # Check for game over
        self._check_win_condition()

        # Clear event state
        self.current_event = None
        self.player_selections = {}

        # Set phase based on game state
        if self.phase == "game_over":
            return  # Keep game_over phase
        else:
            self.phase = "play"

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

    