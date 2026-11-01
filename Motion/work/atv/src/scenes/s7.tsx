// S7 Финал: постер на закате + призыв писать в Direct
import {interpolate, useCurrentFrame, AbsoluteFill} from 'remotion';
import {Photo, Glow, C, ease, fontFamily} from '../lib';
export const S7 = () => {
  const f = useCurrentFrame();
  const zoom = interpolate(f, [0, 69], [1.38, 1.12], {easing: ease});
  const contact = interpolate(f, [10, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <Photo src="a.jpg" cut="a-cut.png" bgZoom={zoom / 1.04} bgBlur={4} fx={0.55} fy={0.6} zoom={zoom} sx={540} sy={1060} filter="contrast(1.12) saturate(1.15)">
        <Glow x={0.555} y={0.575} r={110} color="#ffffff" o={0.7} />
        <Glow x={0.82} y={0.555} r={95} color="#ffffff" o={0.7} />
        <Glow x={0.74} y={0.5} r={80} color={C.red} o={0.6} />
      </Photo>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(8,8,10,0.55) 0%, transparent 28%, transparent 62%, rgba(8,8,10,0.85) 88%)'}} />
      <div style={{position: 'absolute', top: 1320, width: 1080, textAlign: 'center', fontFamily, fontWeight: 500,
        fontSize: 78, letterSpacing: 3, color: C.white, opacity: contact, transform: `translateY(${(1 - contact) * 30}px)`,
        textShadow: '0 4px 20px rgba(0,0,0,0.8)'}}>
        ПО ВСЕМ ВОПРОСАМ<br /><span style={{color: C.gold, fontSize: 78}}>ПИСАТЬ В DIRECT</span>
      </div>
    </>
  );
};
