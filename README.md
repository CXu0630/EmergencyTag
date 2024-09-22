# EmergencyTag
## Inspiration
The first few minutes after a critical medical emergency are crucial for trying to save the patient. We wanted to propose a product that can earn medical teams a few precious minutes to save someone's life. 

## What it does
EmTag is a secure framework that stores emergency medical information on wearable NFC tags. In critical situations where the wearer is unconscious, EmTag provides lifesaving information to medical personnel. 

The EmTag software provides reading and writing capabilities to wearable NFC tags. It stores the user's name, blood type, emergency contact number, birth date, allergies, and medical history all within an NFC tag. It also encrypts the data with AES-CTR cryptography so that sensitive data is not readable by anyone other than medical personnel with access to the EmTag software. 

EmTag is a game-changer for vulnerable groups such as those prone to seizures, the elderly, and children. It can also enhance safety for travelers separated from their party, those engaging in extreme sports, and many others.

## How we built it
EmTag is a Python full-stack software. We used Python's libraries to ensure functionality for complex processes such as monitoring connections to our NFC reader software and handling cryptographic operations. We also made use of PyQt for the front end. 

EmTag is built and tested with the ACS ACR122U NFC card reader. Tags used during development are NTAG213 stickers with 137 bytes of memory each. We specifically selected smaller tags with less storage to make our design more compact.
