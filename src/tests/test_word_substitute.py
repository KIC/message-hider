from word_substitution import create_key, recover_word


def test_word_substitute():
    original_text = "hund katze maus elefant giraffe maise otter"
    substitution = "Apfel Birne Banane Kirsche Dattel Nuss Orange"

    key = create_key(original_text, substitution)

    print(f"\n{recover_word(original_text, key)}\n{substitution}\n{key}\n")
    assert recover_word(original_text, key) == substitution, "Substitution failed"
