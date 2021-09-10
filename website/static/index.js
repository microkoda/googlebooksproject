function importbook(title, authors, published, isbn, pages, thumbnail, language) {
  fetch("/importbook", {
    method: "POST",
    body: JSON.stringify({ title:title, authors:authors, published:published, isbn:isbn, pages:pages,thumbnail:thumbnail,language:language}),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deletebook(isbn) {
  fetch("/deletebook", {
    method: "POST",
    body: JSON.stringify({isbn:isbn}),
  }).then((_res) => {
    window.location.href = "/";
  });
}
