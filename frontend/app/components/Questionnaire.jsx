"use client";
import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import {
  Button,
  Input,
  Card,
  CardBody,
  ScrollShadow,
  Modal,
  ModalFooter,
  ModalBody,
  ModalHeader,
  ModalContent,
} from "@nextui-org/react";
import toast, { Toaster } from "react-hot-toast";

const Questionnaire = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [interaction, setInteraction] = useState("");
  const [isLastQuestion, setIsLastQuestion] = useState(false);
  const [finalReport, setFinalReport] = useState("");
  const [loading, setLoading] = useState(false);
  const [userInput, setUserInput] = useState("");
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [video, setVideo] = useState(null);

  useEffect(() => {
    fetchNextInteraction([]);
  }, []);

  const fetchNextInteraction = async (history) => {
    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:5000/api/next_question",
        {
          chat_history: formatChatHistory(history),
        }
      );
      const data = await response.data;
      const { nextInteraction, isLastQuestion, finalReport } = data;

      if (isLastQuestion) {
        setIsLastQuestion(true);
        setFinalReport(finalReport);
        setShowFileUpload(true);
      } else {
        setInteraction(nextInteraction);
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { role: "assistant", content: nextInteraction },
        ]);
      }
    } catch (error) {
      toast.error("An error occurred while fetching the next interaction.");
      console.error("Error fetching next interaction:", error);
    }
    setLoading(false);
  };

  const formatChatHistory = (history) => {
    return history.map((entry) => `${entry.role}: ${entry.content}`).join("\n");
  };

  const handleResponse = async () => {
    const userResponse = userInput.trim();
    const newHistory = [
      ...chatHistory,
      { role: "user", content: userResponse },
    ];
    setChatHistory(newHistory);
    setUserInput("");
    await fetchNextInteraction(newHistory);
  };

  const handleFileChange = (event) => {
    setSelectedFiles(Array.from(event.target.files));
  };

  const handleAnalyse = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      selectedFiles.forEach((file) => {
        formData.append("files", file);
      });
      formData.append("general_information", finalReport);

      const response = await axios.post(
        "http://127.0.0.1:5000/api/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        }
      );
      const data = response.data;
      const url = URL.createObjectURL(new Blob([data], { type: "video/mp4" }));
      setVideo(url);
    } catch (error) {
      toast.error("An error occurred during analysis.");
      console.error("Error during analysis:", error);
    }
    setLoading(false);
  };

  return (
    <motion.div
      className="flex items-center justify-center min-h-screen"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Toaster />
      <Card className="w-full max-h-screen max-w-md p-4 shadow-2xl">
        <CardBody>
          <motion.h2
            className="text-2xl font-bold text-center mb-6 text-gray-800"
            initial={{ y: -20 }}
            animate={{ y: 0 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            Medical Assistant Chatbot
          </motion.h2>
          <ScrollShadow className="h-[400px] overflow-y-auto mb-4">
            {chatHistory.map((entry, index) => (
              <motion.div
                key={index}
                className={`mb-4 p-3 rounded-lg ${
                  entry.role === "assistant"
                    ? "bg-blue-100 ml-4"
                    : "bg-green-100 mr-4"
                }`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <p
                  className={`text-sm ${
                    entry.role === "assistant"
                      ? "text-blue-700"
                      : "text-green-700"
                  }`}
                >
                  <strong>
                    {entry.role === "assistant" ? "Assistant" : "You"}:
                  </strong>
                </p>
                <p className="mt-1 text-gray-700">{entry.content}</p>
              </motion.div>
            ))}
          </ScrollShadow>
          {showFileUpload ? (
            <motion.div
              className="space-y-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <p className="text-center text-gray-700 mb-2">
                Would you like to upload any images or videos for visual
                information?
              </p>
              <input
                type="file"
                onChange={handleFileChange}
                multiple
                accept="image/*,video/*"
                className="w-full p-2 border rounded"
              />
              <Button
                color="primary"
                onClick={handleAnalyse}
                disabled={loading || selectedFiles.length === 0}
                className="w-full"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-5 h-5 border-t-2 border-b-2 border-white rounded-full animate-spin mr-2"></div>
                    Analysing...
                  </div>
                ) : (
                  "Analyse"
                )}
              </Button>
            </motion.div>
          ) : (
            <motion.div
              className="space-y-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Input
                fullWidth
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Your Response"
                disabled={loading}
                className="bg-gray-50"
              />
              <Button
                color="primary"
                onClick={handleResponse}
                disabled={loading}
                className="w-full"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-5 h-5 border-t-2 border-b-2 border-white rounded-full animate-spin mr-2"></div>
                    Processing...
                  </div>
                ) : (
                  "Submit"
                )}
              </Button>
            </motion.div>
          )}
        </CardBody>
      </Card>
      <Modal isOpen={video !== null} onClose={() => setScore(null)}>
        <ModalContent>
          <ModalHeader>
            <h3 className="text-xl font-semibold">Analysis Result</h3>
          </ModalHeader>
          <ModalBody>
            <video width="600" controls>
              <source src={video} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onClick={() => setScore(null)}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </motion.div>
  );
};

export default Questionnaire;
