from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io 
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder(): #Load voice encoder model
    return VoiceEncoder()

def get_voice_embedding(audio_bytes): #returns the voice embedding of a audio input
    try:
        encoder = load_voice_encoder()
        audio,sr = librosa.load(io.BytesIO(audio_bytes),sr=16000) #Higher sr , better audio
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist() #256 dim embedding
    except Exception as e:
        st.error('Voice recog error')
        return None
    
def identify_speaker(new_embedding, candidates_dict,threshold= 0.65):
    if not new_embedding or not candidates_dict:
        return None, 0.0
    best_sid = None
    best_score = -1.0
    for sid,embedding in candidates_dict.items():
        if embedding:
            score = np.dot(new_embedding,embedding)
            if score > best_score:
                best_score=score
                best_sid= sid
    if best_score >= threshold:
        return best_sid,best_score
    return None, best_score

def process_bulk_audio(audio_bytes, candidate_dict, threshold=0.65): # We'll split the audio in segments and then process each segment
    try:
        encoder = load_voice_encoder()
        audio,sr =librosa.load(io.BytesIO(audio_bytes))
        segments = librosa.effects.split(audio,top_db=30) #top_db is a sensitivity param , higher the value means it catches only high freq voice 
        identified_results = {}
        for start,end in segments:
            if (end-start) < sr*0.5: #a very small segment means it is probably a garbage audio so ignore it 
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)
            sid,score = identify_speaker(embedding,candidate_dict,threshold)
            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score
        return identified_results
    except Exception as e:
        st.error('Bulk process error')
        return None