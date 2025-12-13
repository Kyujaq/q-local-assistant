# Work Helper Feature

**Status:** Planning / Future  
**Created:** 2025-12-13  
**Priority:** Medium (post-MVP)

## Overview

The work helper feature enables the assistant to observe and assist the user during work on a laptop by:
- **Watching the screen** via HDMI capture dongle
- **Listening to audio** via sound output → sound input passthrough
- **Controlling the laptop** using Windows voice commands via TTS
- **Providing proactive assistance** (booking meetings, correcting mistakes, document help, reminders, insights)

## Hardware Setup

```
┌─────────────┐
│   Laptop    │
│ (Work PC)   │
└──────┬──────┘
       │
       ├─HDMI Output───────────────────┐
       │                               │
       └─Audio Output (3.5mm/USB)──────┤
                                       │
                                ┌──────▼──────┐
                                │ HDMI Capture │
                                │   Dongle     │
                                │              │
                                │ Audio Input  │
                                └──────┬───────┘
                                       │
                                ┌──────▼──────┐
                                │   glad0s    │
                                │  (Server)   │
                                │             │
                                │ - Vision    │
                                │ - Audio In  │
                                │ - TTS Out   │
                                └─────────────┘
```

## Use Cases

### 1. Meeting Booking
- Assistant watches screen during work meetings
- Detects mention of future meetings or deadlines
- Books copies of work meetings in personal calendar
- Optionally sends reminder before meeting

### 2. Error Correction
- Observes user typing/editing documents
- Detects typos, formatting issues, or logical errors
- Offers corrections proactively or on request

### 3. Document Assistance
- Watches document editing (Word, Excel, code)
- Suggests improvements, formatting, or content
- Answers questions about document structure

### 4. Reminders & Insights
- Tracks project plans shown on screen
- Reminds user of upcoming deadlines or action items
- Provides insights on project status

### 5. Laptop Control via Voice Commands
- Assistant speaks Windows voice commands via TTS
- Example flow:
  ```
  Assistant (TTS): "Open Excel"
  [Windows hears TTS via audio passthrough]
  Assistant (TTS): "Select cell A1"
  Assistant (TTS): "Type 'Project Budget'"
  ```

## Agent Team Requirements

**Why Multiple Agents:**
- **Vision Agent**: Process screen capture, OCR, layout understanding
- **Audio Agent**: Listen to work meetings, transcribe
- **Planning Agent**: Decide what actions to take (book meeting, offer help, etc.)
- **Control Agent**: Generate voice command sequences for laptop control
- **Coordinator Agent**: Orchestrate the team, manage state

**Coordination Challenges:**
- Real-time screen processing (low latency required)
- Context switching (user working on multiple tasks)
- Permission model (what's okay to watch/record/control)
- Privacy (no recording sensitive data)

## Privacy & Security

**Critical Considerations:**
- **Screen capture**: Should be opt-in, with visual indicator
- **Audio recording**: Must respect work policies (no recording confidential meetings)
- **Laptop control**: Requires explicit permission per action
- **Data retention**: Screen captures and audio should not be permanently stored unless user requests
- **Isolation**: Work data stays separate from personal data

**Proposed Model:**
- User toggles "work helper mode" on/off
- Visual indicator on server (LED or screen notification) when active
- All captured data encrypted and deleted after session unless saved
- No cloud transmission of work data

## Technical Architecture

### Components

1. **HDMI Capture Service**
   - Captures video frames from laptop
   - Runs OCR and layout analysis
   - Feeds Vision Agent

2. **Audio Passthrough Service**
   - Receives laptop audio output
   - Passes to server's audio input
   - Enables TTS control of laptop

3. **Vision Agent (Letta)**
   - Analyzes screen captures
   - Detects text, UI elements, context
   - Stores observations in memory

4. **Control Agent (Letta)**
   - Generates voice command sequences
   - Sends TTS commands to laptop via audio out
   - Monitors success/failure of commands

5. **Coordinator Agent (Letta)**
   - Receives user requests ("Help me with this spreadsheet")
   - Queries Vision Agent for context
   - Tasks Control Agent to execute actions
   - Manages multi-step workflows

### Example Workflow: Book a Meeting

```
1. User in work meeting says: "Let's meet again next Tuesday at 2pm"
2. Audio Agent transcribes, detects meeting mention
3. Coordinator Agent asks Vision Agent: "What meeting is this?"
4. Vision Agent reads screen: "Project X Kickoff - Teams window open"
5. Coordinator Agent asks user (via voice): "Should I book 'Project X Follow-Up' for next Tuesday 2pm?"
6. User: "Yes"
7. Coordinator Agent tasks Control Agent: Open personal calendar, create event
8. Control Agent sends TTS commands to laptop:
   - "Open Calendar"
   - "New Event"
   - "Type 'Project X Follow-Up'"
   - etc.
9. Coordinator confirms booking to user
```

## Integration Points

- **Home Assistant**: Use existing voice I/O infrastructure
- **Vision Processing**: OCR (Tesseract), layout analysis (custom model or API)
- **TTS**: Existing TTS service, routed to laptop audio input
- **Calendar**: Personal calendar API (Google Calendar, Outlook, etc.)

## Open Questions

- [ ] Which HDMI capture dongle supports real-time processing?
- [ ] How to handle laptop audio passthrough reliably (USB audio interface?)
- [ ] What's the latency requirement for real-time assistance?
- [ ] How to prevent feedback loop (assistant hears itself via laptop audio)?
- [ ] What's the permission model for different types of assistance?
- [ ] Should vision processing run on PC (when available) for better performance?

## Dependencies

- **Vision models**: OCR + layout understanding (requires research)
- **Audio infrastructure**: Reliable passthrough without latency
- **TTS service**: High-quality, natural voice (for laptop control)
- **Multi-agent coordination**: Letta dev team must implement orchestration patterns first

## Decision Log

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| 2025-12-13 | Document feature for future reference | User mentioned it; capture before forgotten | Reference for future implementation |

## Next Steps

**Not immediate** - this is a post-MVP feature. Priorities:
1. Complete core assistant (voice, memory, Home Assistant)
2. Validate Letta multi-agent coordination patterns
3. Prototype vision processing pipeline
4. Research HDMI capture hardware options
5. Design permission model with user
6. Implement incrementally (vision → control → coordination)
