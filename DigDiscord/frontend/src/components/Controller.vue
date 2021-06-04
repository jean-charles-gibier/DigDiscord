<template>
  <div class="hello">
  <!-- <h1>{{ value }}</h1> -->
  <h2>Brève note d'intention du projet 13</h2>
    <em>
    Avec Digdiscord, je teste la mise en place d’un service web selon un principe architectural très simple :<br>
    le découplage entre le «front» et le «back».<br>
    A l’instar du motif architectural MVC qui distingue les 3 responsabilités d’un logiciel (Modèle, Vue et Contrôleur), la conception de ce service web peut simplement se définir ainsi (*):<br><br>
    <ul class="list-group list-group-flush">
      <li>
        Récupérer de l’information.<br>
      </li>
      <li>
        Délivrer des services.<br>
      </li>
      <li>
        Avoir une interface accessible.<br>
      </li>
    </ul><br>
Ces objectifs sont remplis par les actions respectives :<br><br>
    <ul class="list-group list-group-flush">
      <li>
        Collecte des commentaires, URL, "snipets", utilisateurs, dates, etc. dans un forum Discord grâce à son <a href='https://discord.com/developers/docs/'>API ouverte</a>.<br>
      </li>
      <li>
        Génération des agrégats analytiques ou ludiques.<br>
      </li>
      <li>
        Présentation l’information sous forme dynamique de listes ou de graphiques.<br>
      </li>
    </ul><br>
En outre, chacune de ces actions correspond à une solution technique bien déterminée :<br><br>
    <ul class="list-group list-group-flush">
      <li>
La collecte est effectuée par une <a href='https://docs.djangoproject.com/fr/3.1/howto/custom-management-commands/'>«commande managée»</a> de Django<br>
Cette commande peut être automatisée par un mécanisme tiers (ex : par cron)<br>
      </li>
      <li>
Les agrégats sont générés naturellement via l’ORM de Django (**) et sont transmis à la couche présentation par les sérialiseurs DRF<br>
      </li>
      <li>
Les données sont exposées via l'API DRF (<a href='https://jean-charles-gibier.org/api/swagger/'>exposée ici</a>)<br>
      </li>
      <li>
L’information est restituée sous forme de graphiques Vue-JS ou de «cards bootstrap»<br>
      </li>

    </ul><br>
Le projet est donc basé sur ce triptyque : Django, DRF, Vue-JS<br>
Plus précisément la pile technique de ce projet comprend :<br><br>
    <ul class="list-group list-group-flush">
      <li>
Django / Django Rest Framework<br>
      </li>
      <li>
Vue-JS<br>
      </li>
      <li>
Bootstrap-vue<br>
      </li>
      <li>
VueChart-Js<br>
      </li>
      <li>
Axios<br>
      </li>
      <li>
Swagger-ui<br>
      </li>
    </ul><br>
+ accessoirement pour l’aspect "bonnes pratiques" :<br><br>
    <ul class="list-group list-group-flush">
      <li>
pre-commit<br>
      </li>
    </ul><br>
    </em>
  <small>
    (*) Enfin moi je le définis ainsi, mais vous pouvez voir ça comme une reformulation du paradigme MVC.<br>
    (**) Je n’ai pas su éviter quelques requêtes SQL brutes (on verra pourquoi)<br>
  </small>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Bienvenue dans cabane du vieux developpeur'
    }
  },
  mounted () {
  },
  components: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
a {
  color: #42b983;
}
li {
    padding-left: 2rem;
}
ul {
    padding-left: 2rem;
}
</style>
