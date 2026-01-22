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
        self.main_deck, self.event_deck, self.fan_deck = decks  # event_deck kept for backwards compat but unused
        self.discard_pile: List[Any] = []  # Cards discarded from play
        self.round = 1  # Tracks rounds (1 round = both players have taken a turn)
        self.current_player_index = 0  # Always 0 (player 1) or 1 (computer), alternates each turn within round
        self.phase = "play"  # "play", "game_over"

        # Event state (player-controlled, not automatic)
        self.current_event: Optional[Any] = None
        self.event_owner: Optional[int] = None  # Which player played the event
        self.event_played_on_round: Optional[int] = None  # Which round the event was played
        self.player_selections: Dict[int, Dict[str, Any]] = {}  # {player_index: {star, stat}}

        # Turn-based play tracking (resets each individual turn, not round)
        self.stars_played_this_turn: Dict[int, int] = {0: 0, 1: 0}  # {player_index: count}
        self.powers_played_this_turn: Dict[int, int] = {0: 0, 1: 0}  # {player_index: count}
        self.events_played_this_turn: Dict[int, int] = {0: 0, 1: 0}  # {player_index: count}

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
            replace_star_index = payload.get("replace_star_index")  # For replacing stars when board is full

            logger.info(f"PLAY_CARD dispatch: player_index={player_index}, hand_index={hand_index}, target_star_index={target_star_index}, replace_star_index={replace_star_index}")

            if 0 <= player_index < len(self.players):
                player = self.players[player_index]
                logger.info(f"Player: {player.name}, hand size: {len(player.hand)}, board size: {len(player.star_cards)}")

                # Validate hand_index and get the card
                if hand_index is None or hand_index < 0 or hand_index >= len(player.hand):
                    logger.warning(f"Invalid hand index {hand_index} for player {player.name}")
                    return self.snapshot()

                card = player.hand[hand_index]
                logger.info(f"Card to play: {card.name} (type: {type(card).__name__})")

                # Check turn limits based on card type
                from engine.models.cards import StarCard, PowerCard, StealStarCard, EventCard
                if isinstance(card, EventCard):
                    # Event card detected - handle event playing
                    logger.info(f"EventCard detected: {card.name}")

                    # Check event play limit
                    if self.events_played_this_turn[player_index] >= 1:
                        logger.warning(f"Player {player.name} already played an event this turn")
                        return self.snapshot()

                    # Check if there's already an active event
                    if self.current_event is not None:
                        logger.warning(f"Cannot play event - {self.current_event.name} is already active")
                        return self.snapshot()

                    # Check if player has stars to compete with
                    if len(player.star_cards) == 0:
                        logger.warning(f"Cannot play event - {player.name} has no stars")
                        return self.snapshot()

                    # Require immediate star selection (target_star_index)
                    if target_star_index is None or target_star_index < 0 or target_star_index >= len(player.star_cards):
                        logger.warning(f"Must select a star to compete in event")
                        return self.snapshot()

                    selected_star = player.star_cards[target_star_index]

                    # Check if star is exhausted
                    if selected_star.exhausted:
                        logger.warning(f"Cannot use exhausted star {selected_star.name} for event")
                        return self.snapshot()

                    # Set up event state
                    self.current_event = card
                    self.event_owner = player_index
                    self.event_played_on_round = self.round

                    # Auto-select stat for event owner based on event type
                    chosen_stat = self._get_stat_for_event(card, selected_star)

                    # Store owner's selection
                    self.player_selections[player_index] = {
                        "star": selected_star,
                        "stat": chosen_stat
                    }

                    # Remove event card from hand
                    player.hand.pop(hand_index)

                    # Track event play
                    self.events_played_this_turn[player_index] += 1

                    logger.info(f"{player.name} played event '{card.name}' with star '{selected_star.name}' using stat '{chosen_stat}'")

                elif isinstance(card, StarCard):
                    logger.info(f"Star card detected, stars played this turn: {self.stars_played_this_turn[player_index]}")
                    if self.stars_played_this_turn[player_index] >= 1:
                        logger.warning(f"Player {player.name} already played a star this turn")
                        return self.snapshot()

                    # Check board limit
                    max_stars = GAME_CONFIG["max_stars_on_board"]
                    logger.info(f"Board limit check: current={len(player.star_cards)}, max={max_stars}, replace_star_index={replace_star_index}")
                    if len(player.star_cards) >= max_stars:
                        if replace_star_index is None:
                            logger.warning(f"Board full ({max_stars} stars) - must specify replace_star_index")
                            return self.snapshot()
                        if replace_star_index < 0 or replace_star_index >= len(player.star_cards):
                            logger.warning(f"Invalid replace_star_index: {replace_star_index}")
                            return self.snapshot()
                        logger.info(f"Board full, will replace star at index {replace_star_index}")

                elif isinstance(card, PowerCard):
                    if self.powers_played_this_turn[player_index] >= 1:
                        logger.warning(f"Player {player.name} already played a power card this turn")
                        return self.snapshot()

                # Special handling for StealStarCard - requires both players
                if isinstance(card, StealStarCard):
                    logger.info("StealStarCard detected - handling steal logic")

                    # Get opponent
                    opponent_index = 1 - player_index
                    opponent = self.players[opponent_index]

                    # Validate opponent has stars
                    if len(opponent.star_cards) == 0:
                        logger.warning(f"Cannot steal - opponent has no stars")
                        return self.snapshot()

                    # Validate target_star_index (opponent's star to steal)
                    if target_star_index is None or target_star_index < 0 or target_star_index >= len(opponent.star_cards):
                        logger.warning(f"Invalid target_star_index for steal: {target_star_index}")
                        return self.snapshot()

                    # Check if stealer's board is full and needs sacrifice
                    max_stars = GAME_CONFIG["max_stars_on_board"]
                    if len(player.star_cards) >= max_stars:
                        if replace_star_index is None:
                            logger.warning(f"Board full ({max_stars} stars) - must specify replace_star_index for sacrifice")
                            return self.snapshot()
                        if replace_star_index < 0 or replace_star_index >= len(player.star_cards):
                            logger.warning(f"Invalid replace_star_index for sacrifice: {replace_star_index}")
                            return self.snapshot()

                    # Perform the steal
                    from engine.rules.power_ops import steal_star_from_opponent
                    steal_star_from_opponent(
                        stealing_player=player,
                        victim_player=opponent,
                        hand_index=hand_index,
                        opponent_star_index=target_star_index,
                        sacrifice_star_index=replace_star_index,
                        discard_pile=self.discard_pile
                    )

                    # Track power play
                    self.powers_played_this_turn[player_index] += 1

                # Otherwise, delegate to common_ops which handles all card types
                else:
                    logger.info(f"Calling play_card_from_hand with replace_star_index={replace_star_index}")
                    play_card_from_hand(player, hand_index, target_star_index=target_star_index,
                                      replace_star_index=replace_star_index, discard_pile=self.discard_pile)
                    logger.info(f"play_card_from_hand completed. Player hand size: {len(player.hand)}, board size: {len(player.star_cards)}")

                    # Track the play (only for non-steal cards - steal tracking happens above)
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
        """Handle end of turn in new sequential system

        Flow:
        - Player presses "End Turn"
        - Check if active event needs resolution (owner's turn coming up)
        - Resolve event if needed
        - Advance to next player's turn
        - Check win condition
        """
        current_player = self.players[self.current_player_index]
        logger.info(f"Ending turn for {current_player.name} (Round {self.round}, Player {self.current_player_index})")

        # Check if there's an active event that needs resolution
        # Event resolves at the END of the turn BEFORE the event owner's next turn
        # So if owner is player 0, resolve when player 1 ends their turn
        # If owner is player 1, resolve when player 0 ends their turn
        next_player_index = (self.current_player_index + 1) % 2

        if self.current_event and self.event_owner is not None and next_player_index == self.event_owner:
            logger.info(f"Event owner's turn is next - resolving event before their turn")
            self._resolve_current_event()

        # Advance to next player's turn
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
        """Advance to next player's turn in sequential system"""
        # Move to next player
        self.current_player_index = (self.current_player_index + 1) % 2

        # Reset play counters for the NEW current player
        self.stars_played_this_turn[self.current_player_index] = 0
        self.powers_played_this_turn[self.current_player_index] = 0
        self.events_played_this_turn[self.current_player_index] = 0

        # If we just advanced to player 0, a full round completed
        if self.current_player_index == 0:
            self.round += 1
            logger.info(f"Round {self.round} started")

        next_player = self.players[self.current_player_index]
        logger.info(f"Now {next_player.name}'s turn (Round {self.round}, Player {self.current_player_index})")

        # Draw card for the player whose turn it is now (respecting hand limit)
        max_hand_size = GAME_CONFIG["max_hand_size"]
        if len(next_player.hand) >= max_hand_size:
            logger.info(f"{next_player.name} hand is full ({max_hand_size} cards) - cannot draw")
        else:
            card = draw_card(self.main_deck)
            if card:
                next_player.hand.append(card)
                logger.info(f"{next_player.name} drew: {card.name}")

        # If computer's turn, have them play automatically
        if self.current_player_index == 1:
            logger.info("Computer AI taking turn...")
            self.computer_ai.take_turn(self)

            # If there's an active event and computer hasn't selected yet, have them select
            if self.current_event and self.event_owner is not None and 1 not in self.player_selections:
                self._computer_select_for_event()

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
                # Note: Event will be resolved in _handle_end_turn(), not here

    def _get_stat_for_event(self, event, star):
        """Get the appropriate stat for an event based on event type

        Args:
            event: The event card
            star: The star card competing

        Returns:
            str: The stat name to use for scoring
        """
        from engine.models.cards import StatContestEvent, DoubleStatEvent

        if isinstance(event, StatContestEvent):
            # Single stat events - use the first (and only) stat option
            if event.stat_options and len(event.stat_options) > 0:
                return event.stat_options[0]
            return "aura"  # Fallback

        elif isinstance(event, DoubleStatEvent):
            # Double stat events - return both stats as a string for logging
            # The actual resolution will sum both stats
            return f"{event.stat1}+{event.stat2}"

        else:
            # Fallback for other event types
            return "aura"

    def snapshot(self) -> Dict[str, Any]:
        return {
            "round": self.round,
            "current_player_index": self.current_player_index,
            "phase": self.phase,
            "current_event": event_view(self.current_event),
            "event_owner": self.event_owner,
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
            "discard_pile_size": len(self.discard_pile),
            "game_over": self.phase == "game_over",
            "winner": self.winner,
            "game_over_reason": self.game_over_reason,
            "fans_to_win": GAME_CONFIG["fans_to_win"],
            "max_stars_on_board": GAME_CONFIG["max_stars_on_board"],
            "max_hand_size": GAME_CONFIG["max_hand_size"]
        }

    