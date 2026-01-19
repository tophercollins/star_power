"""
API Routes for Star Power Game
Endpoints for game creation, card playing, and state management
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import sys
import os
import logging

# Add parent directories to path to import engine modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from services.game_service import GameService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize game service (in-memory for now, will use database later)
game_service = GameService()

# ============================================================================
# Request/Response Models
# ============================================================================

class CreateGameRequest(BaseModel):
    """Request model for creating a new game"""
    player1_name: str = Field(..., min_length=1, max_length=50, description="Player 1 name")
    player2_name: str = Field(default="Computer", max_length=50, description="Player 2 name")

    class Config:
        schema_extra = {
            "example": {
                "player1_name": "Toph",
                "player2_name": "Computer"
            }
        }

class PlayCardRequest(BaseModel):
    """Request model for playing a card"""
    player_index: int = Field(..., ge=0, le=1, description="Player index (0 or 1)")
    hand_index: int = Field(..., ge=0, description="Index of card in player's hand")

    class Config:
        schema_extra = {
            "example": {
                "player_index": 0,
                "hand_index": 2
            }
        }

class SelectStarRequest(BaseModel):
    """Request model for selecting a star for an event"""
    player_index: int = Field(..., ge=0, le=1, description="Player index (0 or 1)")
    star_index: int = Field(..., ge=0, description="Index of star on player's board")
    stat: str = Field(..., description="Stat to use for contest (aura, talent, influence, or legacy)")

    class Config:
        schema_extra = {
            "example": {
                "player_index": 0,
                "star_index": 0,
                "stat": "talent"
            }
        }

class GameResponse(BaseModel):
    """Response model for game data"""
    game_id: str
    state: Dict[str, Any]

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    game_id: Optional[str] = None

# ============================================================================
# Game Endpoints
# ============================================================================

@router.post(
    "/game/create",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new game",
    description="Creates a new Star Power game with two players and returns the initial game state"
)
def create_game(request: CreateGameRequest):
    """
    Create a new game with specified players.

    - **player1_name**: Name for player 1 (required)
    - **player2_name**: Name for player 2 (defaults to "Computer")

    Returns:
    - **game_id**: Unique identifier for the game
    - **state**: Initial game state including players, decks, and starting hands
    """
    try:
        logger.info(f"Creating new game: {request.player1_name} vs {request.player2_name}")

        game_id, state = game_service.create_game(
            player1_name=request.player1_name,
            player2_name=request.player2_name
        )

        logger.info(f"Game created successfully: {game_id}")

        return GameResponse(game_id=game_id, state=state)

    except Exception as e:
        logger.error(f"Error creating game: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create game: {str(e)}"
        )

@router.get(
    "/game/{game_id}/state",
    response_model=Dict[str, Any],
    summary="Get game state",
    description="Retrieves the current state of a game"
)
def get_game_state(game_id: str):
    """
    Get the current state of a game.

    - **game_id**: Unique game identifier

    Returns:
    - Complete game state including players, cards, turn number, and deck information
    """
    try:
        state = game_service.get_game_state(game_id)

        if state is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game not found: {game_id}"
            )

        return state

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting game state for {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get game state: {str(e)}"
        )

@router.post(
    "/game/{game_id}/play_card",
    response_model=Dict[str, Any],
    summary="Play a card",
    description="Play a card from a player's hand"
)
def play_card(game_id: str, request: PlayCardRequest):
    """
    Play a card from a player's hand.

    - **game_id**: Unique game identifier
    - **player_index**: Which player (0 or 1)
    - **hand_index**: Position of card in hand to play

    Returns:
    - Updated game state after the card is played
    """
    try:
        logger.info(f"Playing card in game {game_id}: player={request.player_index}, card={request.hand_index}")

        state = game_service.play_card(
            game_id=game_id,
            player_index=request.player_index,
            hand_index=request.hand_index
        )

        if state is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game not found: {game_id}"
            )

        logger.info(f"Card played successfully in game {game_id}")
        return state

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error playing card in game {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to play card: {str(e)}"
        )

@router.delete(
    "/game/{game_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a game",
    description="Deletes a game (for testing/cleanup)"
)
def delete_game(game_id: str):
    """
    Delete a game.

    - **game_id**: Unique game identifier

    Note: This is primarily for testing and cleanup. In production, games may be archived instead.
    """
    try:
        success = game_service.delete_game(game_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game not found: {game_id}"
            )

        logger.info(f"Game deleted: {game_id}")
        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting game {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete game: {str(e)}"
        )

@router.get(
    "/games/active",
    response_model=Dict[str, Any],
    summary="List active games",
    description="Get a list of all active games (for debugging)"
)
def list_active_games():
    """
    List all active games.

    Returns:
    - **count**: Number of active games
    - **game_ids**: List of game IDs

    Note: This endpoint is primarily for debugging and monitoring.
    """
    try:
        games = game_service.list_games()

        return {
            "count": len(games),
            "game_ids": games
        }

    except Exception as e:
        logger.error(f"Error listing games: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list games: {str(e)}"
        )

@router.post(
    "/game/{game_id}/end_turn",
    response_model=Dict[str, Any],
    summary="End turn",
    description="End the current turn, draw cards, and trigger an event if applicable"
)
def end_turn(game_id: str):
    """
    End the current turn and progress the game state.

    - **game_id**: Unique game identifier

    Returns:
    - Updated game state with new turn number
    - If turn >= 2, an event will be triggered and game phase changes to "event_select"
    """
    try:
        logger.info(f"Ending turn in game {game_id}")

        state = game_service.end_turn(game_id)

        if state is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game not found: {game_id}"
            )

        logger.info(f"Turn ended successfully in game {game_id}")
        return state

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ending turn in game {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to end turn: {str(e)}"
        )

@router.post(
    "/game/{game_id}/select_star",
    response_model=Dict[str, Any],
    summary="Select star for event",
    description="Select which star and stat to use for the current event"
)
def select_star_for_event(game_id: str, request: SelectStarRequest):
    """
    Select a star and stat for the current event.

    - **game_id**: Unique game identifier
    - **player_index**: Which player (0 or 1)
    - **star_index**: Index of star on player's board
    - **stat**: Stat to use (aura, talent, influence, or legacy)

    Returns:
    - Updated game state with player selection recorded
    - If both players have selected, event is automatically resolved
    """
    try:
        logger.info(f"Selecting star for event in game {game_id}: player={request.player_index}, star={request.star_index}, stat={request.stat}")

        state = game_service.select_star_for_event(
            game_id=game_id,
            player_index=request.player_index,
            star_index=request.star_index,
            stat=request.stat
        )

        if state is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game not found: {game_id}"
            )

        logger.info(f"Star selected successfully in game {game_id}")
        return state

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error selecting star in game {game_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to select star: {str(e)}"
        )
