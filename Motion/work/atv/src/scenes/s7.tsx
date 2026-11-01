// S7 Финал: постер на закате, название модели и контакты (заглушки)
import {interpolate, useCurrentFrame, AbsoluteFill} from 'remotion';
import {Photo, Glow, Word, C, ease, fontFamily} from '../lib';
export const S7 = () => {
  const f = useCurrentFrame();
  const zoom = interpolate(f, [0, 69], [1.38, 1.12], {easing: ease});
  const line = interpolate(f, [14, 30], [0, 560], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const contact = interpolate(f, [24, 34], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <Photo src="a.jpg" cut="a-cut.png" bgZoom={1.2 + (zoom - 1.12) * 0.3} bgBlur={4} fx={0.55} fy={0.6} zoom={zoom} sx={540} sy={1060} filter="contrast(1.12) saturate(1.15)">
        <Glow x={0.555} y={0.575} r={110} color="#ffffff" o={0.7} />
        <Glow x={0.82} y={0.555} r={95} color="#ffffff" o={0.7} />
        <Glow x={0.74} y={0.5} r={80} color={C.red} o={0.6} />
      </Photo>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(8,8,10,0.55) 0%, transparent 28%, transparent 62%, rgba(8,8,10,0.85) 88%)'}} />
      <Word text="НАЗВАНИЕ" at={4} y={270} size={150} />
      <Word text="МОДЕЛИ" at={8} y={420} size={150} red />
      <div style={{position: 'absolute', left: 540 - line / 2, top: 590, width: line, height: 10, background: C.red,
        boxShadow: `0 0 24px ${C.red}`}} />
      <div style={{position: 'absolute', top: 1380, width: 1080, textAlign: 'center', fontFamily, fontWeight: 500,
        fontSize: 64, letterSpacing: 3, color: C.white, opacity: contact, transform: `translateY(${(1 - contact) * 30}px)`,
        textShadow: '0 4px 20px rgba(0,0,0,0.8)'}}>
        +7 000 000-00-00<br /><span style={{color: C.gold, fontSize: 52}}>@КОНТАКТЫ</span>
      </div>
    </>
  );
};
