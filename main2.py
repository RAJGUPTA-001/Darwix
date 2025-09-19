import asyncio
from utils import (
    generateaudio_basic,
    generateaudio_top, 
    generateaudio_basic_ssml,
    generateaudio_gtts_emotion,
    generateaudio_all_methods,
)

async def run_choice(choice, text):
    """Run the chosen option asynchronously (in parallel if needed)."""
    try:
        if choice == "1":
            print("🔊 Generating basic TTS...")
            await asyncio.to_thread(generateaudio_basic, text)

        elif choice == "2":
            print("🔊 Generating premium TTS...")
            await asyncio.to_thread(generateaudio_top, text)

        elif choice == "3":
            print("🔊 Generating SSML-enhanced TTS (no LLM)...")
            await asyncio.to_thread(generateaudio_basic_ssml, text)

        elif choice == "4":
            print("🔊 Generating emotion-aware gTTS...")
            await asyncio.to_thread(generateaudio_gtts_emotion, text)

        elif choice == "5":
            print("🔊 Generating all methods in parallel...")
            await asyncio.gather(
                asyncio.to_thread(generateaudio_basic, text),
                asyncio.to_thread(generateaudio_top, text),
                asyncio.to_thread(generateaudio_basic_ssml, text),
                asyncio.to_thread(generateaudio_gtts_emotion, text),
            )

        print("✅ Audio generation completed!\n")

    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    print("🎭 Enhanced Emotion-Aware Text-to-Speech System")
    print("=" * 50)

    while True:
        print("\nChoose an option:")
        print("1. Basic Google Cloud TTS")
        print("2. Premium Google Cloud TTS (Chirp3-HD)")
        print("3. SSML-Enhanced TTS (Direct Generation - No LLM)")
        print("4. Emotion-Aware gTTS with Audio Effects")
        print("5. Generate All Methods")
        print("0. Exit")

        choice = input("\nEnter your choice (0-5): ").strip()

        if choice == "0":
            print("👋 Goodbye!")
            break

        if choice in ["1", "2", "3", "4", "5"]:
            text = input("\nEnter text to synthesize: ").strip()
            if not text:
                print("❌ Please enter some text.")
                continue
            await run_choice(choice, text)
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
