/**
 * ChatMessage Component
 * Displays a single chat message
 */
'use client';

import { useState, useEffect } from 'react';
import { Message, MessageRole } from '@/types';
import { formatDate } from '@/lib/utils';

interface ChatMessageProps {
  message: Message;
  onSendMessage?: (content: string) => void;
}

export default function ChatMessage({ message, onSendMessage }: ChatMessageProps) {
  const isUser = message.role === MessageRole.USER;
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [instantFeedback, setInstantFeedback] = useState<{
    selectedLetter: string;
    isCorrect: boolean;
    correctLetter: string;
  } | null>(null);

  // Ensure content is always a string
  const safeContent = typeof message.content === 'string' 
    ? message.content 
    : (message.content && typeof message.content === 'object')
      ? JSON.stringify(message.content, null, 2)
      : String(message.content || '');

  // Parse quiz question format
  const parseQuizQuestion = (content: string) => {
    // Check if this is a quiz question (contains A. B. C. D. pattern)
    const hasOptions = /[A-D]\.\s+.+/g.test(content);
    if (!hasOptions || isUser) return null;

    // Extract question and options
    const lines = content.split('\n');
    const questionLines: string[] = [];
    const options: { letter: string; text: string; status?: 'correct' | 'incorrect' | 'normal' }[] = [];
    let feedbackMessage = '';
    let isAnswered = false;
    let correctAnswerLetter = '';
    
    let foundOptions = false;
    for (const line of lines) {
      const trimmedLine = line.trim();
      
      // Extract hidden correct answer marker [CORRECT:X]
      const correctAnswerMatch = trimmedLine.match(/\[CORRECT:([A-D])\]/);
      if (correctAnswerMatch) {
        correctAnswerLetter = correctAnswerMatch[1];
        console.log('[Quiz Parse] Found correct answer:', correctAnswerLetter);
        continue;
      }
      
      // Check for feedback messages
      if (trimmedLine.includes('✅ Correct') || trimmedLine.includes('❌ Incorrect')) {
        feedbackMessage = trimmedLine.replace(/\*\*/g, '');
        isAnswered = true;
        continue;
      }
      if (trimmedLine.includes('Type your answer') || trimmedLine.includes('or \'stop\' to end')) {
        continue;
      }
      
      // Match options with feedback markers (check both line and trimmedLine)
      const correctMatch = trimmedLine.match(/^✅\s*([A-D])\.\s+(.+)$/) || line.match(/^✅\s*([A-D])\.\s+(.+)$/);
      const incorrectMatch = trimmedLine.match(/^❌\s*([A-D])\.\s+(.+)$/) || line.match(/^❌\s*([A-D])\.\s+(.+)$/);
      const normalMatch = trimmedLine.match(/^([A-D])\.\s+(.+)$/);
      
      if (correctMatch) {
        foundOptions = true;
        options.push({ letter: correctMatch[1], text: correctMatch[2].trim(), status: 'correct' });
      } else if (incorrectMatch) {
        foundOptions = true;
        options.push({ letter: incorrectMatch[1], text: incorrectMatch[2].trim(), status: 'incorrect' });
      } else if (normalMatch && !trimmedLine.startsWith('✅') && !trimmedLine.startsWith('❌')) {
        foundOptions = true;
        options.push({ letter: normalMatch[1], text: normalMatch[2].trim(), status: 'normal' });
      } else if (!foundOptions && trimmedLine) {
        questionLines.push(line);
      }
    }

    if (options.length === 4) {
      console.log('[Quiz Parse] Parsed quiz data:', { 
        hasOptions: options.length, 
        feedback: feedbackMessage, 
        isAnswered,
        correctAnswerLetter,
        optionStatuses: options.map(o => `${o.letter}:${o.status}`)
      });
      return {
        question: questionLines.join('\n'),
        options,
        feedback: feedbackMessage,
        isAnswered,
        correctAnswerLetter,
      };
    }
    return null;
  };

  const quizData = parseQuizQuestion(safeContent);

  const handleOptionClick = (letter: string, correctAnswer: string | undefined) => {
    if (onSendMessage && !selectedAnswer && correctAnswer) {
      // INSTANT EVALUATION - No waiting for backend!
      const isCorrect = letter === correctAnswer;
      
      // Set instant visual feedback IMMEDIATELY
      setInstantFeedback({
        selectedLetter: letter,
        isCorrect: isCorrect,
        correctLetter: correctAnswer
      });
      
      // Mark as selected to prevent multiple clicks
      setSelectedAnswer(letter);
      
      // Send answer to backend (for recording/next question)
      onSendMessage(letter);
    }
  };

  // Reset instant feedback when new question loads
  useEffect(() => {
    if (quizData?.isAnswered) {
      // Clear instant feedback when backend response arrives
      setInstantFeedback(null);
    }
  }, [quizData?.isAnswered]);

  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">
        <div className="message-header">
          <span className="message-role">
            {isUser ? 'You' : 'QuizBot'}
          </span>
          <span className="message-time">
            {formatDate(message.timestamp)}
          </span>
        </div>
        {quizData ? (
          <div className="quiz-question">
            <div className="message-text">{quizData.question}</div>
            <div className="quiz-options">
              {quizData.options.map((option) => {
                // Determine button state for INSTANT FEEDBACK
                let buttonStatus = option.status || 'normal';
                
                // If instant feedback is active (user just clicked)
                if (instantFeedback && !quizData.isAnswered) {
                  if (option.letter === instantFeedback.selectedLetter) {
                    // User's selected answer
                    buttonStatus = instantFeedback.isCorrect ? 'correct' : 'incorrect';
                  } else if (option.letter === instantFeedback.correctLetter) {
                    // Show correct answer in green
                    buttonStatus = 'correct';
                  }
                }
                
                return (
                  <button
                    key={option.letter}
                    className={`quiz-option-button ${
                      buttonStatus === 'correct' ? 'quiz-option-correct' :
                      buttonStatus === 'incorrect' ? 'quiz-option-incorrect' : ''
                    }`}
                    onClick={() => !quizData.isAnswered && !selectedAnswer && handleOptionClick(option.letter, quizData.correctAnswerLetter)}
                    disabled={quizData.isAnswered || selectedAnswer !== null}
                  >
                    <span className="option-letter">{option.letter}</span>
                    <span className="option-text">{option.text}</span>
                    
                    {/* Show badges for instant feedback */}
                    {instantFeedback && !quizData.isAnswered && option.letter === instantFeedback.selectedLetter && instantFeedback.isCorrect && (
                      <span className="option-badge option-badge-correct">
                        <span className="badge-icon">✓</span>
                        <span className="badge-text">CORRECT!</span>
                      </span>
                    )}
                    {instantFeedback && !quizData.isAnswered && option.letter === instantFeedback.selectedLetter && !instantFeedback.isCorrect && (
                      <span className="option-badge option-badge-incorrect">
                        <span className="badge-icon">X</span>
                        <span className="badge-text">WRONG</span>
                      </span>
                    )}
                    {instantFeedback && !quizData.isAnswered && option.letter === instantFeedback.correctLetter && option.letter !== instantFeedback.selectedLetter && (
                      <span className="option-badge option-badge-correct">
                        <span className="badge-icon">✓</span>
                        <span className="badge-text">CORRECT!</span>
                      </span>
                    )}
                    
                    {/* Show badges from backend response (after reload) */}
                    {buttonStatus === 'correct' && quizData.isAnswered && (
                      <span className="option-badge option-badge-correct">
                        <span className="badge-icon">✓</span>
                        <span className="badge-text">CORRECT!</span>
                      </span>
                    )}
                    {buttonStatus === 'incorrect' && quizData.isAnswered && (
                      <span className="option-badge option-badge-incorrect">
                        <span className="badge-icon">X</span>
                        <span className="badge-text">WRONG</span>
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
            {/* Instant feedback message */}
            {instantFeedback && !quizData.isAnswered && (
              <div className={`quiz-feedback ${
                instantFeedback.isCorrect ? 'feedback-correct' : 'feedback-incorrect'
              }`}>
                {instantFeedback.isCorrect 
                  ? '✅ Correct!' 
                  : `❌ Incorrect. The correct answer is ${instantFeedback.correctLetter}.`
                }
              </div>
            )}
            {/* Backend feedback message (after reload) */}
            {quizData.feedback && (
              <div className={`quiz-feedback ${quizData.feedback.includes('✅') ? 'feedback-correct' : 'feedback-incorrect'}`}>
                {quizData.feedback}
              </div>
            )}
          </div>
        ) : (
          <div className="message-text">{safeContent}</div>
        )}
      </div>
    </div>
  );
}
