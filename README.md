Crypto Ninja is a robust tool combining encryption and steganography to securely hide sensitive data inside PNG images. By encrypting your information and embedding it invisibly, it ensures your secrets remain safe and undetectable, even under scrutiny.

Without the correct password, **it’s impossible to even confirm that any hidden information exists in the file**. Any attempt to analyze the image will reveal no traceable evidence of embedded data, ensuring total plausible deniability.

1. Data is encrypted using the secure **Salsa20 cipher** with a password and a randomly generated salt, ensuring strong protection.
2. The encrypted data is embedded **into the least significant bits of the image's pixel data** at a random position. This process ensures that the visual integrity of the image is maintained.

Image with embedded data:

![Model](https://raw.githubusercontent.com/JFailt/crypto-ninja/refs/heads/main/lena.png)

Data extraction:

![Model](https://raw.githubusercontent.com/JFailt/crypto-ninja/refs/heads/main/example.png)

Warning: To maximize security and ensure undetectability, it is essential to use source images with high entropy - images featuring a wide variety of colors and intricate details. These high entropy images naturally exhibit significant noise and randomness, rendering changes to the least significant bits completely indistinguishable from normal pixel variations. This makes detection of the embedded data through statistical analysis effectively impossible.
