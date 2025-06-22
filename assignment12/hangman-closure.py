# hangman-closure.py

def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())
        display = ''.join([char if char.lower() in guesses else '_' for char in secret_word])
        print("Current word:", display)
        return set(secret_word.lower()).issubset(set(guesses))

    return hangman_closure


def main():
    secret_word = input("Enter the secret word: ")
    print("\n" * 50)  # Clear the screen

    guess_letter = make_hangman(secret_word)

    while True:
        letter = input("Guess a letter: ").strip()
        if not letter or len(letter) != 1:
            print("Please enter a single letter.")
            continue

        if guess_letter(letter):
            print(f"🎉 Congratulations! You've guessed the word '{secret_word}'!")
            break


if __name__ == "__main__":
    main()
