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
    from PIL import Image as PILImage
    PIL_AVAILABLE = True
except ImportError:
    PILImage = None
    PIL_AVAILABLE = False

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
            try:
                if not isinstance(image, np.ndarray):
                    image = np.frombuffer(image, dtype=np.uint8)
                    image = cv2.imdecode(image, flags=1)
                
                if image is not None:
                    self.image = self.ndarray_to_bytes(image)
            except Exception:
                pass

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
    def _no_library_warning(cls) -> None:
        warnings.warn(
            'No optional libraries are installed. '
            'Using default settings.'
        )

    @classmethod
    def _processing_error_warning(cls, library: str, error: Exception = None) -> None:
        message = f'Failed to process media with {library}.'
        if error is not None:
            message += f' Details: {error}'
        message += ' Using default settings.'
        warnings.warn(message)

    @classmethod
    def from_image(cls, image: bytes) -> typing.Union[ResultMedia, str]:
        if PIL_AVAILABLE:
            try:
                img = PILImage.open(io.BytesIO(image))
                width, height = img.size

                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                img.thumbnail((max(width // 20, 100), max(height // 20, 100)))

                output = io.BytesIO()
                img.save(output, format='JPEG', quality=50)
                return ResultMedia(output.getvalue(), width=width, height=height)
            except Exception as e:
                cls._processing_error_warning('Pillow', e)

        if cv2 is None or np is None:
            cls._no_library_warning()
            return cls._default_thumbnail()

        try:
            if not isinstance(image, np.ndarray):
                image = np.frombuffer(image, dtype=np.uint8)
                image = cv2.imdecode(image, flags=1)

            if image is None:
                raise ValueError('Could not decode image.')

            height, width = image.shape[0], image.shape[1]

            image = cv2.resize(image, (round(width / 20), round(height / 20)), interpolation=cv2.INTER_CUBIC)

            status, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 50])
            if status:
                return ResultMedia(bytes(buffer), width=width, height=height)
        except Exception as e:
            cls._processing_error_warning('OpenCV', e)

        return cls._default_thumbnail()

    @classmethod
    def from_video(cls, video: bytes) -> typing.Union[ResultMedia, str]:

        if VideoFileClip is not None:
            file_name = None
            capture = None
            try:
                with tempfile.NamedTemporaryFile(mode='wb+', suffix='.mp4', delete=False) as file:
                    file.write(video)
                    file_name = file.name

                capture = VideoFileClip(file_name)
                width, height = capture.size
                seconds = int(capture.duration)
                image = capture.get_frame(seconds / 2)
                return ResultMedia(image, width, height, seconds * 1000)
            except Exception as e:
                cls._processing_error_warning('MoviePy', e)
                return cls._default_thumbnail()
            finally:
                if capture is not None:
                    try:
                        capture.close()
                    except Exception:
                        pass
                if file_name and os.path.exists(file_name):
                    try:
                        os.remove(file_name)
                    except Exception:
                        pass

        if cv2 is None:
            cls._no_library_warning()
            return cls._default_thumbnail()

        capture = None
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
        except Exception as e:
            cls._processing_error_warning('OpenCV', e)
        finally:
            if capture is not None:
                try:
                    capture.release()
                except Exception:
                    pass

        return cls._default_thumbnail()

    @classmethod
    def from_manual(cls, data: bytes) -> typing.Union[ResultMedia, str]:
        if PIL_AVAILABLE:
            try:
                img = PILImage.open(io.BytesIO(data))
                width, height = img.size

                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                img.thumbnail((100, 100), PILImage.LANCZOS)

                output = io.BytesIO()
                img.save(output, format='JPEG', quality=30)
                return ResultMedia(output.getvalue(), width=width, height=height)
            except Exception as e:
                cls._processing_error_warning('Pillow', e)

        if cv2 is not None and np is not None:
            try:
                if not isinstance(data, np.ndarray):
                    nparr = np.frombuffer(data, dtype=np.uint8)
                    nparr = cv2.imdecode(nparr, flags=1)
                    if nparr is not None:
                        height, width = nparr.shape[0], nparr.shape[1]
                        nparr = cv2.resize(nparr, (100, 100), interpolation=cv2.INTER_CUBIC)
                        status, buffer = cv2.imencode('.jpg', nparr, [cv2.IMWRITE_JPEG_QUALITY, 30])
                        if status:
                            return ResultMedia(bytes(buffer), width=width, height=height)
            except Exception as e:
                cls._processing_error_warning('OpenCV', e)

        try:
            return cls.from_video(data)
        except Exception:
            pass

        return cls._default_thumbnail()

class Audio:
    @classmethod
    def get_audio_info(cls, audio: bytes) -> AudioResult:
        filename = None
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

        except Exception as e:
            if filename and os.path.exists(filename):
                try:
                    os.remove(filename)
                except Exception:
                    pass
            warnings.warn(f'Failed to process audio metadata. Details: {e} Using default values.')
            return AudioResult(1, '')