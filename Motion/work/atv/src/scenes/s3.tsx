// S3 Профиль: медленный пролёт сбоку, 4×4
import {interpolate, useCurrentFrame} from 'remotion';
import {Photo, Word, Dust} from '../lib';
export const S3 = () => {
  const f = useCurrentFrame();
  const sx = interpolate(f, [0, 39], [620, 470]);
  const zoom = interpolate(f, [0, 39], [1.18, 1.26]);
  return (
    <>
      <Photo src="c.jpg" cut="c-cut.png" bgZoom={1.18} bgDx={(620 - sx) * 0.6} fx={0.5} fy={0.64} zoom={zoom} sx={sx} sy={1080} filter="contrast(1.12) saturate(1.15)" />
      <Dust n={40} seed="s3" o={0.6} />
      <Word text="4×4" at={6} y={360} size={300} />
    </>
  );
};
