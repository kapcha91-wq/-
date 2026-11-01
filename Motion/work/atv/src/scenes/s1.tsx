// S1 Пробуждение: темнота → фары → наезд
import {interpolate, useCurrentFrame, random} from 'remotion';
import {Photo, Glow, C, shake} from '../lib';
export const S1 = () => {
  const f = useCurrentFrame();
  const k = interpolate(f, [0, 45], [0, 1], {extrapolateRight: 'clamp'});
  const zoom = 1.08 + Math.pow(k, 2.2) * 0.42;
  const lightOn = f >= 4 ? (f < 10 ? (random(`fl${f}`) > 0.4 ? 1 : 0.2) : 1) : 0;
  const bright = interpolate(f, [6, 30], [0.06, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const s = shake(f, f > 30 ? 6 : 2, 's1');
  return (
    <Photo src="a.jpg" cut="a-cut.png" bgZoom={1.08 + Math.pow(k, 2.2) * 0.12} fx={0.6} fy={0.58} zoom={zoom} sx={540 + s.x} sy={1000 + s.y}
      filter={`brightness(${bright}) contrast(1.15) saturate(1.1)`}>
      <Glow x={0.555} y={0.575} r={150} color="#ffffff" o={lightOn} />
      <Glow x={0.82} y={0.555} r={130} color="#ffffff" o={lightOn} />
      <Glow x={0.74} y={0.5} r={120} color={C.red} o={lightOn * 0.9} />
    </Photo>
  );
};
