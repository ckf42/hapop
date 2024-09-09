import hashlib
import io
import pathlib

hashFormats: tuple[str, ...] = tuple(
        x
        for x in ('md5', 'sha1', 'sha256')
        if x in hashlib.algorithms_available)

def hex_file_digest(target: io.BufferedReader, hasherName: str) -> str:
    try:
        return hashlib.file_digest(target, hasherName).hexdigest()
    except AttributeError:
        h = hashlib.new(hasherName)
        while (chunk := target.read(h.block_size)):
            h.update(chunk)
        return h.hexdigest()


def main() -> None:
    print("Format:", " ".join(hashFormats))
    filedir: pathlib.Path = pathlib.Path(__file__).resolve(strict=True).parent
    with (filedir / 'target.txt').open('rt') as targetList:
        for line in targetList:
            targetName = line.strip()
            print(targetName)
            targetPath: pathlib.Path = (filedir / targetName).resolve(strict=False)
            if not targetPath.exists():
                print("\tdoes not exist")
            else:
                with (filedir / (targetName + '.hash')).open('wt') as recFile:
                    print("size", targetPath.stat().st_size, file=recFile)
                    for h in hashFormats:
                        with targetPath.open('rb') as targetFile:
                            print(h, hex_file_digest(targetFile, h),
                                  file=recFile)

if __name__ == '__main__':
    main()

