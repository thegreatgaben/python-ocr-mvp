export function readFileAsURL(file: File, callback: (imageResult: string | ArrayBuffer | null) => void) {
  const reader = new FileReader();

  reader.onload = function (e) {
    callback(e.target.result)
  }

  reader.readAsDataURL(file);
}

