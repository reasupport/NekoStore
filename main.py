import subprocess

def run_bot():
    try:
        subprocess.run(["python3", "bot.py"], check=True)
        print("Bot Berhasil Dijalankan")
    except subprocess.CalledProcessError as e:
        print(f"Bot Terpaksa Dihentikan: {e}")
    except KeyboardInterrupt:
        print("Bot Berhasil Dihentikan")

if __name__ == "__main__":
    run_bot()
