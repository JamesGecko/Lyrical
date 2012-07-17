class Song(object):
    def __init__(self):
        self.lyrics = """Amazing Grace, how sweet the sound,
That saved a wretch like me
I once was lost but now am found,
Was blind but now I see.

'Twas Grace that taught
my heart to fear
And Grace, my fears relieved
How precious did that Grace appear
the hour I first believed

Through many dangers, toils and snares
we have already come
'Twas Grace that brought us safe thus far
and Grace will lead us home

The Lord has promised good to me
His word my hope secures
He will my shield and portion be
as long as life endures

When we've been here ten thousand years
bright shining as the sun
We've no less days to sing God's praise
then when we've first begun

Amazing Grace, how sweet the sound
That saved a wretch like me
I once was lost but now am found
Was blind but now I see"""

        self.title = 'Amazing Grace'
        self.copyright = ''

    def lyrics_list(self):
        return self.lyrics.split('\n\n')
