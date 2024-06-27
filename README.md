# Video/Audio editor app

This streamlit app provides an opportunity for users to upload an mp4 file and cut it into parts that users can set in the field "How many clips do you want:", the user also needs to put a prompt for generating audio for one of the clips(user can choose clip in "Choose clip with generated audio:"). Field column num is responsible for the number of in one column on the screen.

# Not using https://github.com/riffusion/riffusion

During development, the provided repository wasn't used, because of the impossibility of running riffusion normally(it starts successfully and accepts POST request, but then generates random error "unexpected keyword argument 'max_iter'"), so it was decided to use gtts. If developers provided Dockerfile, it would make work with riffusion so much easier.
