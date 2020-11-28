gsutil ls "gs://cs410_images/memes/**" | while read objpath; do
    newpath="$(echo $objpath | sed "s#memes/##")"
    gsutil mv "$objpath" "$newpath"
  done