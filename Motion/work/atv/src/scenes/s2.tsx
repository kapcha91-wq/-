// S2 Колесо: удар-наезд, МОЩЬ
import {spring, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Photo, Word, shake} from '../lib';
export const S2 = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: {damping: 16, stiffness: 180}});
  const zoom = interpolate(p, [0, 1], [2.9, 2.2]) + f * 0.004;
  const s = shake(f, f < 8 ? 10 : 2, 's2');
  return (
    <>
      <Photo src="c.jpg" fx={0.235} fy={0.73} zoom={zoom} sx={560 + s.x} sy={1150 + s.y} filter="contrast(1.2) saturate(1.15)" />
      <Word text="МОЩЬ" at={4} y={330} size={260} red />
    </>
  );
};
