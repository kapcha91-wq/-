import React from 'react';
import {AbsoluteFill, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {continueRender, delayRender} from 'remotion';

// Oswald (Google Fonts, OFL) лежит локально в public/fonts — браузер рендера не ходит в интернет
export const fontFamily = 'Oswald';
const fontHandle = delayRender('Loading Oswald');
Promise.all(['500', '700'].map((w) => new FontFace('Oswald', `url(${staticFile(`fonts/Oswald-${w}.ttf`)})`, {weight: w}).load()))
  .then((faces) => { faces.forEach((ff) => document.fonts.add(ff)); continueRender(fontHandle); });

export const C = {bg: '#0E0F12', red: '#E0242E', gold: '#F2A640', white: '#F5F2EC'};
export const ease = Easing.bezier(0.22, 1, 0.36, 1);

/** Photo placed so that image point (fx,fy) (0..1) sits at screen point (sx,sy). zoom 1 = cover 1080x1920.
 *  With `cut` (вырезанный квадроцикл) — два слоя: фон (размыт, свой зум/сдвиг) и квадроцикл поверх → параллакс. */
export const Photo: React.FC<{
  src: string; fx: number; fy: number; zoom: number; sx?: number; sy?: number; rot?: number;
  filter?: string; children?: React.ReactNode;
  cut?: string; bgZoom?: number; bgDx?: number; bgDy?: number; bgBlur?: number;
}> = ({src, fx, fy, zoom, sx = 540, sy = 960, rot = 0, filter, children, cut, bgZoom, bgDx = 0, bgDy = 0, bgBlur = 5}) => {
  const layer = (z: number, x: number, y: number, img: string, flt: string | undefined, kids?: React.ReactNode) => {
    const W = 1440 * z, H = 1920 * z;
    return (
      <div style={{position: 'absolute', width: W, height: H, left: x - fx * W, top: y - fy * H,
        transformOrigin: `${fx * 100}% ${fy * 100}%`, transform: `rotate(${rot}deg)`}}>
        <Img src={staticFile(img)} style={{width: '100%', height: '100%', filter: flt}} />
        {kids}
      </div>
    );
  };
  return (
    <AbsoluteFill style={{overflow: 'hidden', background: C.bg}}>
      {cut ? (
        <>
          {layer((bgZoom ?? zoom) * 1.04, sx + bgDx, sy + bgDy, src, `${filter ?? ''} blur(${bgBlur}px) brightness(0.85)`)}
          {layer(zoom, sx, sy, cut, `${filter ?? ''} drop-shadow(0 30px 40px rgba(0,0,0,0.55))`, children)}
        </>
      ) : layer(zoom, sx, sy, src, filter, children)}
    </AbsoluteFill>
  );
};

/** Glow in image space (percent coords). */
export const Glow: React.FC<{x: number; y: number; r: number; color: string; o: number}> = ({x, y, r, color, o}) => (
  <div style={{position: 'absolute', left: `${x * 100}%`, top: `${y * 100}%`, width: r * 2, height: r * 2,
    marginLeft: -r, marginTop: -r, borderRadius: '50%', opacity: o, mixBlendMode: 'screen',
    background: `radial-gradient(circle, ${color} 0%, ${color}88 18%, transparent 70%)`}} />
);

/** Cinematic grade shared by every scene: warm top, dark vignette. */
export const Grade: React.FC<{v?: number}> = ({v = 0.75}) => (
  <AbsoluteFill style={{pointerEvents: 'none'}}>
    <AbsoluteFill style={{background: `radial-gradient(ellipse 75% 60% at 50% 50%, transparent 40%, rgba(8,8,10,${v}) 100%)`}} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(242,166,64,0.18) 0%, transparent 35%, transparent 70%, rgba(8,8,10,0.55) 100%)', mixBlendMode: 'multiply'}} />
  </AbsoluteFill>
);

/** One big word that punches in on frame `at`. accent words are red. */
export const Word: React.FC<{text: string; at: number; until?: number; y?: number; size?: number; red?: boolean; x?: number; align?: 'center' | 'left'}> =
  ({text, at, until = 9999, y = 1180, size = 210, red, x = 540, align = 'center'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (f < at || f > until) return null;
  const s = spring({frame: f - at, fps, config: {damping: 14, stiffness: 220}});
  const scale = interpolate(s, [0, 1], [1.35, 1]);
  const out = interpolate(f, [until - 4, until], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', top: y, left: align === 'center' ? 0 : x, width: align === 'center' ? 1080 : undefined,
      textAlign: align, fontFamily, fontWeight: 700, fontSize: size, lineHeight: 1, letterSpacing: 4,
      color: red ? C.red : C.white, opacity: Math.min(s * 1.6, 1) * out,
      transform: `scale(${scale})`, transformOrigin: align === 'center' ? '50% 50%' : '0% 50%',
      textShadow: '0 8px 30px rgba(0,0,0,0.7), 0 2px 0 rgba(0,0,0,0.5)'}}>
      {text}
    </div>
  );
};

/** Golden dust drifting through backlight. */
export const Dust: React.FC<{n?: number; seed?: string; o?: number}> = ({n = 70, seed = 'd', o = 1}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', opacity: o, pointerEvents: 'none'}}>
      {new Array(n).fill(0).map((_, i) => {
        const r = (k: string) => random(`${seed}${i}${k}`);
        const size = 3 + r('s') * 10;
        const x = ((r('x') * 1300 + f * (1 + r('v') * 4)) % 1300) - 110;
        const y = r('y') * 1920 - f * (0.5 + r('u') * 2);
        const blur = r('b') > 0.7 ? 4 : 0.5;
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: size, height: size, borderRadius: '50%',
          background: C.gold, opacity: 0.25 + r('o') * 0.6, filter: `blur(${blur}px)`, boxShadow: `0 0 ${size * 2}px ${C.gold}`}} />;
      })}
    </AbsoluteFill>
  );
};

/** Camera shake offset. */
export const shake = (f: number, amp: number, seed = 's') => ({
  x: (random(`${seed}x${f}`) - 0.5) * 2 * amp, y: (random(`${seed}y${f}`) - 0.5) * 2 * amp,
});

/** Flash overlay peaking at frame `at`. */
export const Flash: React.FC<{at: number; color?: string; len?: number}> = ({at, color = '#fff', len = 6}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at - len, at, at + len], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{background: color, opacity: o, pointerEvents: 'none'}} />;
};
