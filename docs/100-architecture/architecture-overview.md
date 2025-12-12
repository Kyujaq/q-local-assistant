# Architecture Overview

## Purpose
This project aims to build a home-integrated personal assistant with real reasoning, memory, voice capabilities, proactive behavior, and limited vision features. The system also supports workflows that help with day-to-day tasks and parts of the user's work life.

## System Users
- **Primary user:** the owner (for now).
- **Future users:** family, guests, and other contexts with distinct capability sets and permissions.

## High-Level Components

### Server (glad0s: GTX 1070 + K80)
Always-on machine responsible for:
- Core orchestrator (assistant brain routing).
- Letta agents (assistant logic, memory layers, tools).
- Home Assistant integrations (events, automations, satellite devices).
- Audio/STT/TTS pipelines.
- Vision preprocessing workloads (K80 GPU).
- Tailscale-connected satellite endpoints (Pi, mobile).
- Integration and system tests.
- Night crew executor (controller of dev agents).
- Stable, low-latency runtime for daily assistant operation.

### PC (RTX 4070 Ti Super)
High-performance dev-and-processing machine:
- **Coding-S** model (~7B) for fast editing/refactor/autocomplete tasks.
- **Coding-L** model (~14–30B) for deep reasoning, architecture, tests, and nightly heavy tasks.
- Optional Slot M / Slot L for assistant reasoning when PC is idle.
- Dev agents (Architect, Coder, Tester, Documentation, Reviewer).
- Heavy offline tasks orchestrated by the server's night crew.
- May be busy (gaming) or asleep; system adapts via fallback logic.

### External Integrations
- **Home Assistant** (core sensor/event/control layer).
- **Paprika** (recipes, pantry, groceries).
- **Cameras / screen-watch** services.
- **Tailscale** (secure access to satellites and mobile app).
- Additional APIs used in a minimal, security-conscious "local first" philosophy.

## Model Slots (Runtime)
- **Slot S (Small)**: ~7B model running on server for fast reactions, routing, and lightweight tasks.
- **Slot M (Medium)**: ~14–30B core reasoning model (preferred from PC when idle).
- **Slot L (Large)**: deep/slow model for heavy reasoning, planning, multi-file work, and night jobs (PC only).

## Development Architecture Separation
- **Dev system:** dev agents, coding models, test runners — these are part of the *development environment*, not the assistant itself.
- **Runtime system:** orchestrator, Letta agents, automations, memories — these are the *product* the dev team builds.
- Dev team does not "talk" to the assistant except via automated tests.

## Source of Truth
All decisions, architecture, workflows, coding standards, and feature designs are stored in the `docs/` folder.
LLMs rely on these documents, not chat history.
