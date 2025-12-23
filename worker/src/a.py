import asyncio


async def main():
    video_URL = "/watch?v=y2G_ldkimp4&list=RDy2G_ldkimp4&start_radio=1&pp=ygUaVGhpcyBjcmhpc21hcyBBZGVsZSBseXJpY3OgBwE%3D"
    proc = await asyncio.create_subprocess_shell(
        "./yt-dlp_linux_aarch64 -f bestaudio -x --audio-format mp3 --no-playlist -o 'out.mp3' '"
        + video_URL
        + "'",
        cwd="/home/playlogo",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()

    # Optional: inspect output
    if stdout:
        print(stdout.decode(), end="")
    if stderr:
        print(stderr.decode(), end="")

    print("TESt")


asyncio.run(main())
