// S6 Нарезка: фара → люстра → диск, по 12 кадров
import {spring, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Photo, Glow, C} from '../lib';
const cuts = [
  {src: 'a.jpg', fx: 0.56, fy: 0.575, glow: '#ffffff'},
  {src: 'a.jpg', fx: 0.74, fy: 0.5, glow: C.red},
  {src: 'b.jpg', fx: 0.56, fy: 0.735, glow: ''},
];
export const S6 = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const i = Math.min(2, Math.floor(f / 12));
  const lf = f - i * 12;
  const c = cuts[i];
  const p = spring({frame: lf, fps, config: {damping: 18, stiffness: 260}});
  const zoom = interpolate(p, [0, 1], [3.1, 2.5]);
  return (
    <Photo src={c.src} fx={c.fx} fy={c.fy} zoom={zoom} sx={540} sy={1000} filter="contrast(1.2) saturate(1.15)">
      {c.glow && <Glow x={c.fx} y={c.fy} r={160} color={c.glow} o={0.85} />}
    </Photo>
  );
};
