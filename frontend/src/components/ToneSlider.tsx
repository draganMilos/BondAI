import React from 'react';

type Props = { value: number; onChange: (v:number)=>void };
export default function ToneSlider({ value, onChange }: Props){
  return (
    <div style={{margin: '8px 0'}}>
      <label>Tone: cautious ↔ bold</label>
      <input type="range" min={-1} max={1} step={0.1} value={value} onChange={e=>onChange(parseFloat(e.target.value))} />
    </div>
  );
}
