import yaml


class Lary:

    """
    Lary is a small Python 3 tool that enables PGP encryption on PCM audio
    streams. It works by allowing a user to parse WAV frame data as their message
    is being recorded, which enables us to pack and encrypt the resulting byte stream
    immediately after recording. The resulting output is a regular-looking
    (though it is quite lengthy) PGP message that can be delivered to the intended
    recipient via any normal channels.
    """

    def __init__(self):
        try:
            self.config = yaml.load(open('config', 'r'))
        except yaml.YAMLError:
            print("Error in configuration file")

    def new_msg(self):
        """
        Records a new message and receives its PGP string back.
        The string is saved to pgp_msg and it can be passed to other methods
        within the Lary class.
        """
        from send_laryngitis import record_message, encrypt_message
        try:
            rec_msg = record_message()
            print('Recording sampling frequency:  ', str(rec_msg[1]), 'Hz')
        except:
            print("An error has occurred.")
            return
        else:
            pgp_msg = encrypt_message(rec_msg[0])
            print("pgp_msg saved.")
            return pgp_msg

    def play_msg(self, pgp_msg):
        """
        Sends a pgp_msg to receive() and get a file back.
        """
        from receive_laryngitis import play_message
        import subprocess as sp
        import tempfile as tf
        print("We're gonna decrypt some secrets.")
        # create a temporary file using a context manager
        try:
            fgpg = open(tf.NamedTemporaryFile().name, 'wb')
            fgpg.write(bytes(pgp_msg + "\n", "ascii"))
        except IOError:
            print("ERROR: The file could not be opened.")
            return
        else:
            gpg_cmd = ['gpg', '-d', 'encrypted.message']
            try:
                fp = open(tf.NamedTemporaryFile().name, 'wb')
                fp_msg = sp.check_output(gpg_cmd)
                fp.write(bytes(fp_msg))
                fp.seek(0)
            except:
                print("An error occurred!")
            else:
                print("Beginning message playback.")
                play_proc = play_message(fp.name)
                print("Find your message at file:  ", play_proc)
            finally:
                fp.close()
        finally:
            fgpg.close()
