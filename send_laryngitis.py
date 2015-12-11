import getpass
import pgpy
import pickle
import pyaudio
import soundfile as sf
import wave

# DO NOT EDIT: #
CHUNK = 1024
FORMAT = pyaudio.paInt32  # paInt16  |  paInt8
CHANNELS = 2
RATE = 96000  # sample rate
RECORD_SECONDS = 7
WAVE_OUTPUT_FILENAME = "output.wav"
MSG_FILENAME = "message.asc"
################


def record_message():
    """
    Run this method to open up the system's default audio input and write it to
    a buffer. It will create a PCM stream as per the specifications provided in
    the settings at the top of the script.
    """
    # Record audio and extract all incoming frame data
    p = pyaudio.PyAudio()
    try:
        frames = []
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("* recording")
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)  # 2 bytes(16 bits) per channel
        print("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
    except IOError:
        print('Could not write stream!')
        return
    # Write the stream out
    try:
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    except wf.Error:
        print('Frames violate WAVE specifications!')
        return
    data, samplerate = sf.read(WAVE_OUTPUT_FILENAME)
    return [data, samplerate]


def encrypt_message(edata, to_file=True):
    """
    This guy takes data created by the record_message method and shoves it into
    a msgpack stream. Then we PGP-encrypt that msgpack stream and sign it.
    """
    d = edata.tolist()
    key, _ = pgpy.PGPKey.from_file(PGP_KEY_PATH)
    sec, _ = pgpy.PGPKey.from_file(PGPRIV_PATH)
    try:
        f = open(WAVE_OUTPUT_FILENAME, 'wb')
        pickle.dump(d, f)
    finally:
        f.close()
    # Write PGP-encrypted stream to disk
    file_message = pgpy.PGPMessage.new(WAVE_OUTPUT_FILENAME, file=True)
    assert sec.is_protected
    assert sec.is_unlocked is False
    print('Enter key passphrase to sign your message:  ')
    key_password = getpass.getpass()
    with sec.unlock(key_password):
        assert sec.is_unlocked
        file_message |= sec.sign(file_message)
        msgstr = str(file_message)
    if to_file:
        print('We will write the communication to file:  ', MSG_FILENAME)
        msg = open(MSG_FILENAME, 'wt')
        msg.write(msgstr)
        msg.close()
    return msgstr  # ASCII Armored
