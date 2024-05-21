import hashlib
import pathlib

hashFormats: tuple[str, ...] = tuple(
        x
        for x in ('md5', 'sha1', 'sha256')
        if x in hashlib.algorithms_available)

def main() -> None:
    print("Format:", " ".join(hashFormats))
    filedir: pathlib.Path = pathlib.Path(__file__).resolve(strict=True).parent
    with (filedir / 'target.txt').open('rt') as target:
        for line in target:
            targetName = line.strip()
            print(targetName)
            with (filedir / (targetName + '.hash')).open('wt') as recFile:
                for h in hashFormats:
                    with (filedir / targetName).open('rb') as targetFile:
                        print(h, hashlib.file_digest(targetFile, h).hexdigest(),
                              file=recFile)

if __name__ == '__main__':
    main()
