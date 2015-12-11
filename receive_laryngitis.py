import pickle
import soundfile as sf

# DO NOT EDIT:
################
CHUNK = 1024
RATE = 96000
INPUT_MSG_FILENAME = 'decrypted.message'
DECR_OUTPUT_FILENAME = '_decr.wav'
################


def play_message(in_msg_fn):
    """
    This method opens a decrypted in_msg and converts the data to an audio
    stream. Then, it simply reads in the frames of the audio file and writes
    the data to an output stream. In other words, it plays the message for you.
    """
    try:
        in_msg = open(in_msg_fn, 'rb')
        data = pickle.load(in_msg)
        in_msg.close()
        print('Data pickled')
    except IOError:
        print("ERROR: Failed to open message file.")
        return
    sf.write(DECR_OUTPUT_FILENAME, data, samplerate=RATE)
    ##########################################################################
    # For now, I just want to make sure the WAV file is written successfully.#
    # Until then, this playback stuff will be on the backlog.#################
    ##########################################################################
    # wf = wave.open(DECR_OUTPUT_FILENAME, 'rb')
    # p = pyaudio.PyAudio()
    # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    #                 channels=wf.getnchannels(),
    #                 rate=wf.getframerate(),
    #                 output=True)
    # data = wf.readframes(CHUNK)
    # while data != '':
    #     stream.write(data)
    #     data = wf.readframes(CHUNK)
    # stream.stop_stream()
    # stream.close()
    # p.terminate()
    return DECR_OUTPUT_FILENAME
