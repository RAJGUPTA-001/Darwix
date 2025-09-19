import sys
import asyncio
from utils import generateaudio_top, generateaudio_basic, generateaudio_basic_ssml

async def main():
    if len(sys.argv) < 2:
        print("Usage: python cli_runner.py 'Your text here'")
        sys.exit(1)

    input_text = " ".join(sys.argv[1:])

    await asyncio.gather(
        asyncio.to_thread(generateaudio_top, input_text),
        asyncio.to_thread(generateaudio_basic, input_text),
        asyncio.to_thread(generateaudio_basic_ssml, input_text),
    )
    print("✅ Audio generation complete. Files saved as output_top.mp3, output_basic.mp3, output_basic_ssml.mp3")

if __name__ == "__main__":
    asyncio.run(main())
