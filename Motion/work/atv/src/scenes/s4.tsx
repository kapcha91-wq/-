// S4 Перед: красная дуга, блик, ЛЕБЁДКА
import {interpolate, useCurrentFrame, AbsoluteFill} from 'remotion';
import {Photo, Word} from '../lib';
export const S4 = () => {
  const f = useCurrentFrame();
  const zoom = interpolate(f, [0, 36], [1.75, 1.9]);
  const sweep = interpolate(f, [6, 26], [-700, 1500], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <Photo src="b.jpg" fx={0.25} fy={0.64} zoom={zoom} sx={560} sy={1080} filter="contrast(1.15) saturate(1.15)" />
      <AbsoluteFill style={{mixBlendMode: 'screen', pointerEvents: 'none'}}>
        <div style={{position: 'absolute', left: sweep, top: -300, width: 160, height: 2600, transform: 'rotate(24deg)',
          background: 'linear-gradient(90deg, transparent, rgba(255,240,220,0.55), transparent)', filter: 'blur(8px)'}} />
      </AbsoluteFill>
      <Word text="ЛЕБЁДКА" at={4} y={330} size={190} />
    </>
  );
};
