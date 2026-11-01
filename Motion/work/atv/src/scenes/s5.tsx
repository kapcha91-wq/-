// S5 Бездорожье: протектор, пыль, ГРЯЗЬ → НЕ ПРЕПЯТСТВИЕ
import {interpolate, useCurrentFrame} from 'remotion';
import {Photo, Word, Dust, shake} from '../lib';
export const S5 = () => {
  const f = useCurrentFrame();
  const zoom = interpolate(f, [0, 39], [2.1, 2.3]);
  const s = shake(f, 2.5, 's5');
  return (
    <>
      <Photo src="a.jpg" fx={0.4} fy={0.78} zoom={zoom} sx={560 + s.x} sy={1150 + s.y} filter="contrast(1.2) saturate(1.1) brightness(0.95)" />
      <Dust n={110} seed="s5" />
      <Word text="ГРЯЗЬ" at={2} until={19} y={330} size={260} />
      <Word text="НЕ" at={20} y={250} size={130} />
      <Word text="ПРЕПЯТСТВИЕ" at={22} y={390} size={150} red />
    </>
  );
};
