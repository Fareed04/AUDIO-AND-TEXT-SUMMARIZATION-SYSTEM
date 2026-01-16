# 🎧 Audio and Text Summarization System

## 📌 Project Overview

This project is a **web-based audio and text summarization system** developed as my final-year applied project. The system is designed to process **long-form audio recordings and large text documents**, transforming them into concise, decision-ready summaries through user-configurable summarization options.

A key demonstration of the system’s capability was successfully summarizing **over 40 minutes of historical audio from the Jonestown Massacre**, validating its effectiveness on lengthy, real-world audio content that would be impractical to review manually.

---

## 🎯 Problem Statement

Long-form audio recordings and extensive text documents are time-consuming to review, making it difficult for users to quickly extract key insights. This challenge is especially pronounced in academic research, journalism, investigations, and archival analysis, where recordings can span **30–60+ minutes**.

---

## 🧠 Objectives

* Enable summarization of **both audio and text inputs** within a single system
* Support **long-duration audio processing (40+ minutes)** without manual intervention
* Provide users with control over:

  * **Summarization type:** Extractive or Abstractive
  * **Summary length:** Short, Medium, or Long
* Deliver readable, structured summaries suitable for rapid understanding

---

## 🛠️ Tools & Technologies

* **Programming Language:** Python
* **Backend Framework:** Flask
* **Audio Processing:** Speech-to-text pipeline for audio transcription
* **NLP & Summarization:** Transformer-based and extractive summarization techniques
* **Development Environment:** PyCharm
* **Frontend:** HTML/CSS for user interaction

---

## ⚙️ System Workflow

1. **Audio/Text Input**

   * Users upload an audio file or paste text directly into the application.

2. **Audio Transcription (for audio inputs)**

   * Long-form audio (including 40+ minute recordings) is converted into text using a speech-to-text pipeline.

3. **Preprocessing & Cleaning**

   * Transcribed and text-based inputs are cleaned, normalized, and segmented to improve summarization quality.

4. **Summarization Engine**

   * Users select:

     * **Extractive summarization** (key sentence selection)
     * **Abstractive summarization** (semantic rewriting)
   * Users also choose summary length: **Short, Medium, or Long**.

5. **Output Generation**

   * The system generates and displays a structured summary optimized for readability and quick comprehension.

---

## 📊 Results & Key Capabilities

* Successfully summarized **40+ minutes of Jonestown Massacre audio**, demonstrating scalability to long recordings
* Enabled flexible summarization with **multiple output lengths and methods**
* Reduced review time for long audio content from **40+ minutes to a few minutes of reading**
* Delivered consistent summaries across both audio-derived and text-based inputs

---

## 🚀 Future Enhancements

* Speaker diarization for multi-speaker audio
* Timestamped summaries linked back to original audio segments
* Support for additional file formats and larger datasets
* Performance optimization for near real-time summarization

---

## 📚 Academic Context

This project was developed as part of my **BSc Computer Science (Information Systems)** program and demonstrates applied skills in:

* Natural Language Processing
* Audio-to-text pipelines
* Backend system design
* Applied AI for real-world information compression
