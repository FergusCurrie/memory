import React, { useState } from 'react';
import api from '../api';

// const postResult = async (id: string, correct: boolean) => {
//     var data = JSON.stringify({
//       card: id,
//       result: correct,
//     });
//     console.log(data);
//     try {
//       const res = await api.post('/api/flashcard/put_result/', data, {
//         headers: {
//           'Content-Type': 'application/json',
//         },
//       });
//     } catch (error) {
//       alert(error);
//     }
//   };

const AddCards: React.FC = () => {
  const [front, setFront] = useState('');
  const [back, setBack] = useState('');

  const handleAddCard = async () => {
    console.log('trying to add card');
    try {
      const response = await api.post('/api/cards', {
        question: front,
        answer: back,
      });
      console.log('Card added:', response.data);
      setFront('');
      setBack('');
      alert('Card added successfully!');
    } catch (error) {
      console.log(error);
      alert(error);
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        maxWidth: '500px',
        margin: 'auto',
      }}
    >
      <h1>Add Cards</h1>
      <textarea
        value={front}
        onChange={(e) => setFront(e.target.value)}
        placeholder="Front of card"
        rows={5}
        style={{ padding: '10px', fontSize: '16px' }}
      />
      <textarea
        value={back}
        onChange={(e) => setBack(e.target.value)}
        placeholder="Back of card"
        rows={5}
        style={{ padding: '10px', fontSize: '16px' }}
      />
      <button
        onClick={handleAddCard}
        style={{ padding: '10px', fontSize: '16px', cursor: 'pointer' }}
      >
        Add Card
      </button>
    </div>
  );
};

export default AddCards;
