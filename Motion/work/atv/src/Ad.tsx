import {AbsoluteFill, Sequence, interpolate, useCurrentFrame} from 'remotion';
import {Grade, Flash, C} from './lib';
import {S1} from './scenes/s1';
import {S2} from './scenes/s2';
import {S3} from './scenes/s3';
import {S4} from './scenes/s4';
import {S5} from './scenes/s5';
import {S6} from './scenes/s6';
import {S7} from './scenes/s7';

// Сцены (кадры при 30 к/с): границы — удары музыки
export const T = {s1: 0, s2: 45, s3: 81, s4: 120, s5: 156, s6: 195, s7: 231, end: 300};

const Shutter: React.FC<{at: number}> = ({at}) => {
  const f = useCurrentFrame();
  const x = interpolate(f, [at - 7, at + 7], [-1400, 1400], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (f < at - 7 || f > at + 7) return null;
  return <div style={{position: 'absolute', left: x - 300, top: -400, width: 1600, height: 2800, background: C.red,
    transform: 'rotate(18deg)', boxShadow: `0 0 80px ${C.red}`}} />;
};

const Blackout: React.FC<{at: number}> = ({at}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at - 6, at, at + 4], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{background: '#000', opacity: o}} />;
};

export const Ad = () => {
  const seq = [S1, S2, S3, S4, S5, S6, S7];
  const starts = [T.s1, T.s2, T.s3, T.s4, T.s5, T.s6, T.s7, T.end];
  return (
    <AbsoluteFill style={{background: C.bg}}>
      {seq.map((S, i) => (
        <Sequence key={i} from={starts[i]} durationInFrames={starts[i + 1] - starts[i]}><S /></Sequence>
      ))}
      <Grade />
      <Flash at={T.s2} len={2} />
      <Shutter at={T.s3} />
      <Blackout at={T.s4} />
      <Flash at={T.s5} len={2} />
      <Flash at={T.s7} color={C.gold} len={3} />
    </AbsoluteFill>
  );
};
