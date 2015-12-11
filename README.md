# Lary

This is a work-in-progress app meant to allow for safe voice communication over standard message delivery channels. By using **PGP** we are able to record voice messages, sign and pack their audio data with a powerful PGP encryption tool such as `gpg`. Intended message receipients can decrypt and play back this message. The messages are intended to be temporary, and are shredded from the file system upon closing the application.

## Send short PGP-encrypted voice messages over the web

With Lary, you can record a user's voice message up to 7 seconds in length and securely transit it to a recipient using their PGP public key.

## How It Works

Lary is comprised of (currently) two modules - `send_laryngitis.py` and `receive_laryngitis.py`. Use the former to record and encrypt the message. Use the latter to decrypt the message and play the resulting file back.

**Please note that your ALSA configuration will make or break this code! Ensure that the default audio recording and playback devices on your machine are configured to point to an actual, accessible audio device.**

### send_laryngitis.py

After recording the audio, `send_laryngitis.py` will store a messagepacked version of the resulting byte stream. Then, it encrypts the packed WAV frames using a provided PGP public key.

### receive_laryngitis.py

The recipient of a message must decrypt the data with their PGP private key and save it to the provided filename within the script's code. After loading in the decrypted msgpack byte stream, `receive_laryngitis.py` will then unpack the frames back into a WAV file. The `play_message()` method will provide a sound buffer to play back the recording.

## Dependencies

This here is a Python 3 application. So, make sure you're running that on your system. Then, get the module dependencies:

`pip install msgpack-python pyaudio numpy pysoundfile pgpy pyyaml` 

## Status

This code is really just a proof of concept. Because I am not widely experienced in cryptography, I would gladly accept anyone's offer for assistance in developing this further along into maturity. The free and open web needs a safe and really instantaneous means for voice communication, so I will take whatever help I can get!

## Use

#### Getting Started

Open up the `receive_laryngitis.py` and `send_laryngitis.py` files, and edit the global values at the top of both files.

**NOTE**: To record in ALSA, you must set the RATE value to the same setting as your ALSA config. This means it's probably going to be either 41000 or 48000 -- maybe 96000 if you're cool like me.

#### Record a new signed PGP-encrypted voice message

Open your favored Python shell and:

```
In [1]: from lary import Lary  # Import the Lary class

In [2]: l = Lary()
Hey! Let's share some secrets.

In [3]: pgpmsg = l.new_msg()  # Record a new voice message from the default microphone input on the system

* recording
* done recording
Enter key passphrase to sign your message:  YourCleverPGPPassphrase
pgp_msg saved.
```

Your PGP string will then be accessible from `pgpmsg`.

#### Play back a message

You can play back any pgp_msg intended for your ears with `l.play(pgp_msg)`

## Problems

There are many. The highest priority is to ensure that my encryption/decryption methods are sane and effective. I will likely discover many holes in my own ideas, and I would love for others to poke holes of their own! Please reach out to me if you see any security flaws.

* The code isn't doing a lot to gracefully fail. I will get around to adding that in, I promise.
* We are recording in stereo but I think we should be summing to mono for transmission. Need to test this on some two-channel mobile implementations such as those in iOS devices.

## Looking Ahead

I have many goals for the future of Lary.

* Change the project name to Lary when the project is far enough along.
* Enable OPUS audio as default audio file that gets encrypted and sent to the recipient. Less exploitable than WAV and also much better file sizes.
* Create a CLI app that interfaces with this code to give users a real-world implementation of the concept.
