import {Composition} from 'remotion';
import {Ad} from './Ad';
export const RemotionRoot = () => (
  <Composition id="AtvAd" component={Ad} durationInFrames={300} fps={30} width={1080} height={1920} />
);
