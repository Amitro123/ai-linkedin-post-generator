# API Setup Guide

## Problem
Your Gemini API key is for Google AI Studio, but CrewAI/LiteLLM routes `gemini/` models to Vertex AI (which requires different authentication).

## Solutions

### Option 1: Use OpenAI (Recommended - Best Quality)
1. Go to https://platform.openai.com/api-keys
2. Create an API key
3. Add to `.env`:
```
OPENAI_API_KEY=sk-proj-...your-key-here
```
4. Cost: ~$0.15 per 1M input tokens (very cheap for gpt-4o-mini)

### Option 2: Use Groq (Free & Fast)
1. Go to https://console.groq.com/keys
2. Create a free account and API key
3. Add to `.env`:
```
GROQ_API_KEY=gsk_...your-key-here
```
4. Free tier: 30 requests/minute, very fast responses

### Option 3: Fix Gemini (Advanced)
To use your Gemini API key properly, you need to install `google-generativeai` and use it directly instead of through LiteLLM. This requires code changes.

## Current Status
The code will try OpenAI first, then fall back to Groq. Add one of these API keys to continue.
