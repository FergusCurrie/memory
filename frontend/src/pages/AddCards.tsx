import React, { useState } from 'react';
import api from '../api';

const AddCards: React.FC = () => {
  const [front, setFront] = useState('');
  const [back, setBack] = useState('');
  const [cardType, setCardType] = useState('basic');

  const handleAddCard = async () => {
    console.log('trying to add card');
    try {
      const response = await api.post('/api/card/cards', {
        question: front,
        answer: back,
        type: cardType,
      });
      console.log('Card added:', response.data);
      setFront('');
      setBack('');
      setCardType('basic');
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
      <select
        value={cardType}
        onChange={(e) => setCardType(e.target.value)}
        style={{ padding: '10px', fontSize: '16px' }}
      >
        <option value="basic">Basic</option>
        <option value="code">Code</option>
        <option value="definition">Definition</option>
      </select>
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
