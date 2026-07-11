"""
Media processing module for thumbnails and audio metadata.
"""
import io
import os
import typing
import base64
import tempfile
import mutagen
import warnings

DEFAULT_THUMB_BASE64 = "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"

try:
    from moviepy.editor import VideoFileClip
except (ImportError, RuntimeError):
    VideoFileClip = None

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

try:
    import PIL.Image
except ImportError:
    PIL = None


class ResultMedia:
    def __repr__(self) -> str:
        return repr(vars(self))

    def __init__(self,
                 image: bytes,
                 width: typing.Optional[int] = 200,
                 height: typing.Optional[int] = 200,
                 seconds: typing.Optional[int] = 1) -> None:
        self.image = image
        self.width = width
        self.height = height
        self.seconds = seconds

        if hasattr(cv2, 'imdecode'):
            if not isinstance(image, np.ndarray):
                image = np.frombuffer(image, dtype=np.uint8)
                image = cv2.imdecode(image, flags=1)

            self.image = self.ndarray_to_bytes(image)

    def ndarray_to_bytes(self, image, *args, **kwargs) -> str:
        if hasattr(cv2, 'resize'):
            self.width = image.shape[1]
            self.height = image.shape[0]

            image = cv2.resize(
                image,
                (round(self.width / 20), round(self.height / 20)),
                interpolation=cv2.INTER_CUBIC)

            status, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 50])
            if status is True:
                return io.BytesIO(buffer).read()

    def to_base64(self) -> str:
        return base64.b64encode(self.image).decode('utf-8')


class AudioResult:
    def __init__(self, duration: int = 1, performer: str = '') -> None:
        self.duration = duration
        self.performer = performer


class MediaThumbnail:
    @classmethod
    def _default_thumbnail(cls) -> str:
        return DEFAULT_THUMB_BASE64

    @classmethod
    def from_image(cls, image: bytes) -> typing.Union[ResultMedia, str]:
        if PIL is not None:
            try:
                img = PIL.Image.open(io.BytesIO(image))
                width, height = img.size

                img.thumbnail((max(width // 20, 100), max(height // 20, 100)))
                
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=50)
                return ResultMedia(output.getvalue(), width=width, height=height)
            except Exception:
                pass

        if cv2 is None or np is None:
            warnings.warn('OpenCV or NumPy not found, using default thumbnail.')
            return cls._default_thumbnail()

        try:
            if not isinstance(image, np.ndarray):
                image = np.frombuffer(image, dtype=np.uint8)
                image = cv2.imdecode(image, flags=1)

            height, width = image.shape[0], image.shape[1]

            image = cv2.resize(image, (round(width / 20), round(height / 20)), interpolation=cv2.INTER_CUBIC)

            status, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 50])
            if status:
                return ResultMedia(bytes(buffer), width=width, height=height)
        except Exception:
            pass

        return cls._default_thumbnail()

    @classmethod
    def from_video(cls, video: bytes) -> typing.Union[ResultMedia, str]:

        if VideoFileClip is not None:
            try:
                with tempfile.NamedTemporaryFile(mode='wb+', suffix='.mp4', delete=False) as file:
                    file.write(video)
                    file_name = file.name

                capture = VideoFileClip(file_name)
                width, height = capture.size
                seconds = int(capture.duration)
                image = capture.get_frame(seconds / 2)
                capture.close()
                os.remove(file_name)
                return ResultMedia(image, width, height, seconds * 1000)
            except Exception as e:
                print(f"Error processing video with moviepy: {e}")
                if os.path.exists(file_name):
                    os.remove(file_name)
                return cls._default_thumbnail()

        if cv2 is None:
            warnings.warn('OpenCV not found, using default thumbnail.')
            return cls._default_thumbnail()

        try:
            with tempfile.NamedTemporaryFile(mode='wb+', suffix='.mp4') as file:
                file.write(video)

                capture = cv2.VideoCapture(file.name)
                total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
                middle_frame_index = total_frames // 2
                capture.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_index)
                status, image = capture.read()

                if status is True:
                    fps = capture.get(cv2.CAP_PROP_FPS)
                    seconds = int(total_frames / fps) * 1000
                    width = image.shape[1]
                    height = image.shape[0]

                    return ResultMedia(image, width, height, seconds)
        except Exception:
            pass

        return cls._default_thumbnail()


class Audio:
    @classmethod
    def get_audio_info(cls, audio: bytes) -> AudioResult:
        try:
            with tempfile.NamedTemporaryFile('wb', suffix='.rpa', delete=False) as file:
                file.write(audio)
                filename = file.name

            audio_file = mutagen.File(filename, easy=True)
            performer = ''
            duration = 1

            if audio_file is not None:
                duration = int(audio_file.info.length) if hasattr(audio_file.info, 'length') else 1

                try:
                    performer = audio_file.tags.get('artist', [''])[0]
                except (AttributeError, KeyError, IndexError, TypeError):
                    pass

            os.remove(filename)
            return AudioResult(duration, performer)

        except Exception:
            return AudioResult(1, '')