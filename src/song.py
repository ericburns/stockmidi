import random

from midiutil.MidiFile import MIDIFile


class Song(object):

    def __init__(self, name, song_data, tempo=120):
        self.name = name
        self.tempo = tempo
        self.song_data = song_data
        self.tracks = []

        self.init_tracks()

    def init_tracks(self):
        for track_number, (track_id, track_data) in enumerate(self.song_data.iteritems()):
            track = Track(
                number=track_number,
                name=track_id,
                track_data=track_data,
                tempo=self.tempo
            )
            self.tracks.append(track)

    def generate(self):
        for track in self.tracks:
            track.generate()

    def write(self, filename):
        midi = MIDIFile(len(self.tracks))

        for track in self.tracks:
            track.write(midi)

        with open(filename, 'wb') as outf:
            midi.writeFile(outf)


class Track(object):

    def __init__(self, number, name, track_data, tempo):
        self.number = number
        self.name = name
        self.tempo = tempo
        self.track_data = track_data
        self.notes = []

        self.init_notes()

    def init_notes(self):
        stock_series = [x['in_stock'] for x in self.track_data['events']]

        # Create a note series by note length and start time
        note_series = []
        note_starts_at = None
        note_length = 0
        for time, in_stock in enumerate(stock_series):
            if not in_stock:
                if note_starts_at is None:
                    note_starts_at = time
                note_length += 1
            else:
                if note_starts_at is not None:
                    note_series.append((note_starts_at, note_length))
                    note_starts_at = None
                    note_length = 0

        # Generate all the notes based on the series
        for start_time, note_length in note_series:
            note = Note(
                track_number=self.number,
                channel=0,
                start=start_time,
                duration=note_length
            )
            self.notes.append(note)

    def generate(self):
        for note in self.notes:
            note.generate()

    def write(self, midi):
        midi.addTrackName(self.number, 0, self.name)
        midi.addTempo(self.number, 0, self.tempo)

        for note in self.notes:
            note.write(midi)


class Note(object):

    def __init__(self, track_number, channel, start, duration):
        self.track_number = track_number
        self.channel = channel
        self.pitch = None
        self.start = start
        self.duration = duration
        self.volume = 100

    def generate(self):
        # Make longer notes lower, more often
        high_end = (127 - self.duration)
        self.pitch = random.uniform(0, high_end)

    def write(self, midi):
        assert self.pitch is not None, 'must generate a note first'
        midi.addNote(self.track_number, self.channel, self.pitch, self.start, self.duration, self.volume)
