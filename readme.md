The GPS.py, cam.py, and screen_load.py are all built to run on the raspberry pi 4 system with their requisite dependencies. The .jpg imgaes are testing images used as part of our proof of concept.
The image_capture.py can be used to retireved server stored images to the local device.

HealthyHat (gemini_api dir)
A mobile-first grocery shopping companion that helps you shop smarter, eat healthier, and find what you need in-store.

Features
🛒 Shopping Assistant — Point your phone's camera at any item and ask questions. AI identifies products and shares price, nutrition, and usage tips.
🎙️ Voice-first — Talk to the assistant hands-free with built-in speech-to-text and text-to-speech.
📋 Smart Grocery Lists — Build and manage your shopping list on the go.
🗺️ Store Locator — Find nearby stores with directions.
👨‍🍳 Recipe Chat — Get recipe ideas and cooking guidance from an AI chef.
🏪 Manager Portal — Store managers can view and update store-level info.
Tech Stack
Frontend: React 19 + TanStack Start + Tailwind CSS v4
Backend: Lovable Cloud (auth, database, edge functions)
AI: Google Gemini via Lovable AI Gateway
Voice: Browser-native Web Speech API
Getting Started

bun install
bun run dev
