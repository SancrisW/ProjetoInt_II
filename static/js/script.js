fetch('http://servicodados.ibge.gov.br/api/v3/noticias/?qtd=10',  {
    method: "GET"
  })
  .then((res) => res.json())
  .then((data) => {
     console.log(data)

     
     document.querySelector("#TESTE").innerHTML += data.items.map((item)=>{
        let img = JSON.parse(item.imagens)
        return(`<div class="Noticia_Cont"> 
        <img src="https://agenciadenoticias.ibge.gov.br/${img.image_intro}"> 
            <p>${item.titulo}</p>
        <a href='${item.link}' target="_blank"> link </a></div>`)
     })

     /*document.querySelector("#TESTE2").innerHTML= data.items[0].introducao*/
})
  .catch((err) => {
    console.log(err);
  });