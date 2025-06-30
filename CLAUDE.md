# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
PolyVoxCord is a Discord bot for text-to-speech functionality with support for multiple Japanese TTS engines (VOICEROID2, VOICEVOX, SofTalk).

## Development Commands

### Setup
```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Initialize database
python app/init_db.py

# Run the bot
python app/main.py
```

### Code Quality
```bash
# Format imports
isort .

# Format code
black .

# Lint code
flake8
```

## Architecture Overview

The codebase follows a layered architecture:

1. **Bot Layer** (`app/base/bot.py`): Core bot class extending discord.py's commands.Bot
   - Manages per-guild read queues with message ordering guarantee
   - Handles voice channel connections and audio playback
   - Implements resource cleanup on disconnect
2. **Cogs** (`app/cogs/`): Command groups implementing Discord slash commands
   - Each cog represents a feature domain (read, connection, settings, etc.)
3. **Service Layer** (`app/service/`): Business logic and orchestration
   - Services handle complex operations and coordinate between repositories
   - `read_service.py`: Manages async voice file creation with Future-based coordination
4. **Repository Layer** (`app/repository/`): Database access using SQLAlchemy
   - Each repository handles CRUD operations for specific entities
5. **Voice Models** (`app/voice_model/`): TTS engine integrations
   - Each voice model implements the base interface for different TTS engines

## Key Implementation Patterns

### Adding New Commands
New commands should be added as methods in the appropriate cog class using the `@discord.app_commands.command()` decorator.

### Database Operations
- Use repository classes for all database operations
- Sessions are managed via context managers in service layer
- Models are defined in `app/model/` using SQLAlchemy declarative base

### Voice Processing Flow
1. Message received → Queue immediately with Future (`read_service.py`)
2. Async voice creation:
   - Text input → Dictionary replacement (`reading_dict_service.py`)
   - Text processing → MeCab parsing if needed
   - Voice generation → Selected TTS engine (`voice_model/`)
3. Queue processing → Wait for turn based on message ID
4. Audio output → Discord voice channel with proper ordering

### Queue Management Pattern
- Per-guild queues using `asyncio.Queue[tuple[int, asyncio.Future[list[str]]]]`
- Message ordering guaranteed by checking message ID before processing
- Non-matching messages are re-queued to maintain order
- Proper cleanup on guild disconnect with Future cancellation

### Error Handling
- Service layer methods return Result objects or raise specific exceptions
- Cogs handle exceptions and send appropriate Discord embed responses
- Use `ErrorContext` for consistent error formatting
- Voice generation has 30-second timeout with proper Future handling

## Environment Configuration
Required environment variables (.env file):
- `TOKEN`: Discord bot token
- `DB_NAME`: Database file name (default: PolyVoxCord.db)
- `SOFTALK_PATH`: Path to SofTalk executable
- `VOICEVOX_HOST`: VOICEVOX API host
- `VOICEVOX_PORT`: VOICEVOX API port
- `USER_DICT_CSV_PATH`: Path to MeCab user dictionary

## Important Considerations
- All text processing assumes Japanese input
- Voice models have different availability and requirements
- Connection management tracks per-guild voice connections
- User settings persist across servers
- Guild settings are server-specific
- Voice file creation is non-blocking using Future-based async pattern
- Message order is strictly preserved even with async voice generation