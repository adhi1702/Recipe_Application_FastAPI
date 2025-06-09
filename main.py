from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from groq import Groq  # Groq LLM client
import os
from typing import List, Optional

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Recipe data model
class Recipe(BaseModel):
    id: int
    title: str
    ingredients: List[str]
    instructions: str
    image_url: str
    type: str  # "veg" or "non-veg"
    cuisine: str


# Sample recipes data
recipes = [
    Recipe(
        id=1,
        title="Chole (Chickpea Curry)",
        ingredients=["Chickpeas", "Onions", "Tomatoes", "Ginger-Garlic Paste", "Oil", "Cumin Seeds", "Turmeric Powder", "Red Chili Powder", "Coriander Powder", "Garam Masala", "Salt", "Coriander Leaves", "Water"],
        instructions="Chole is a popular North Indian dish made with chickpeas, simmered in a rich and spicy tomato-onion gravy. To make it, soak chickpeas overnight and cook them until soft. In a pan, sauté chopped onions in oil until golden, add ginger-garlic paste, and cook for a minute. Add chopped tomatoes, turmeric, red chili powder, coriander powder, and garam masala. Cook until the oil separates. Add the cooked chickpeas along with some of the water used for boiling, and simmer for 15–20 minutes. Garnish with fresh coriander leaves and serve with rice or bhature.",
        image_url = "static/images/chole.jpg",
        type="veg",
        cuisine="North"
    ),
    Recipe(
        id=2,
        title="Paneer Butter Masala",
        ingredients=["Paneer", "Butter", "Onion", "Tomatoes", "Ginger-Garlic Paste", "Fresh Cream", "Red Chili Powder", "Garam Masala", "Kasuri Methi", "Sugar", "Salt", "Oil", "Water"],
        instructions="Paneer Butter Masala is a creamy and mildly spiced curry. Begin by frying cubes of paneer (Indian cottage cheese) until golden and set aside. In a pan, cook onions, tomatoes, garlic, and ginger until soft, then blend to a smooth paste. Return it to the pan, add butter, cream, a little sugar, and spices like garam masala, red chili powder, and kasuri methi (dried fenugreek leaves). Let it simmer, then gently add the paneer cubes and cook for a few more minutes. Serve hot with naan or jeera rice.",
        image_url = "static/images/paneer_masala.jpg",
        type="veg",
        cuisine="North"
    ),
     Recipe(
        id=3,
        title="Vegetable Biriyani",
        ingredients=["Basmati Rice", "Carrot", "Beans", "Green Peas", "Potatoes", "Onion", "Tomato", "Ginger-Garlic Paste", "Oil", "Cumin Seeds", "Turmeric Powder", "Biryani Masala", "Red Chili Powder", "Salt", "Saffron", "Milk", "Mint Leaves", "Coriander Leaves", "Water"],
        instructions="Vegetable Biryani is a fragrant rice dish layered with spiced vegetables. First, cook basmati rice until 70% done and keep it aside. In a deep pan, sauté sliced onions, garlic, and ginger in ghee or oil, then add chopped vegetables like carrots, beans, and peas. Add biryani masala, turmeric, and chili powder. Once the vegetables are tender, layer them with the rice and sprinkle saffron milk on top. Cover and cook on low heat (dum) for 15–20 minutes. Serve with raita or pickle.",
        image_url = "static/images/veg_biriyani.jpeg",
        type="veg",
        cuisine="South"
    ),
     Recipe(
        id=4,
        title="Masoor Dal (Red Lentil Curry)",
        ingredients=["Masoor Dal", "Onion", "Tomato", "Garlic", "Cumin Seeds", "Turmeric Powder", "Red Chili Powder", "Garam Masala", "Oil", "Salt", "Water", "Coriander Leaves"],
        instructions="Masoor Dal is a comforting lentil dish. Rinse red lentils thoroughly and boil them with turmeric and salt until soft. In a separate pan, heat ghee or oil and temper with cumin seeds, garlic, and chopped onions. Add chopped tomatoes, red chili powder, and garam masala. Once cooked, pour this tempering over the boiled dal and simmer for a few minutes. Garnish with coriander and serve with steamed rice or roti.",
        image_url = "static/images/masoor_dal.jpeg",
        type="veg",
        cuisine="North"
    ),
    Recipe(
    id=5,
    title="Sambar",
    ingredients=["Toor Dal", "Tamarind Pulp", "Drumsticks", "Carrot", "Tomato", "Onion", "Mustard Seeds", "Curry Leaves", "Dry Red Chilies", "Asafoetida", "Turmeric Powder", "Sambar Powder", "Salt", "Oil", "Water", "Coriander Leaves"],
    instructions="Sambar is a lentil-based vegetable stew. Begin by cooking toor dal with turmeric until soft. In a separate pan, boil chopped vegetables like drumsticks, carrots, and tomatoes until tender. Add tamarind pulp and sambar powder and let it simmer. Mix in the mashed dal and adjust the consistency with water. In a small pan, heat oil, splutter mustard seeds, curry leaves, dry red chilies, and a pinch of asafoetida. Pour the tempering over the sambar, garnish with coriander, and serve hot with rice or idli.",
    image_url = "static/images/sambar.jpeg",
    type="veg",
    cuisine="South"
    ),
    Recipe(
    id=6,
    title="Medu Vada",
    ingredients=["Urad Dal", "Onion", "Green Chilies", "Ginger", "Curry Leaves", "Salt", "Oil", "Black Pepper", "Cumin Seeds"],
    instructions="Medu Vada is a crispy South Indian fritter. Soak urad dal for a few hours and grind it into a smooth batter with minimal water. Add finely chopped onions, green chilies, ginger, curry leaves, cumin, and pepper. Shape the batter into doughnut-shaped vadas and deep fry until golden and crisp. Serve hot with coconut chutney and sambar.",
    image_url = "static/images/medu_vadai.jpeg",
    type="veg",
    cuisine="South"
    ),
    Recipe(
    id=7,
    title="Lemon Rice",
    ingredients=["Cooked Rice", "Lemon Juice", "Mustard Seeds", "Urad Dal", "Chana Dal", "Green Chilies", "Ginger", "Curry Leaves", "Turmeric Powder", "Salt", "Oil", "Asafoetida", "Cashews"],
    instructions="Lemon Rice is a tangy and flavorful dish. Heat oil in a pan, splutter mustard seeds, add urad dal, chana dal, green chilies, ginger, curry leaves, asafoetida, and cashews. Once golden, add turmeric and cooked rice. Mix well, sprinkle salt and drizzle lemon juice. Stir gently and serve with pickle or papad.",
    image_url = "static/images/lemon_rice.jpeg",
    type="veg",
    cuisine="South"
    ),
    Recipe(
    id=8,
    title="Gobi Manchurian",
    ingredients=["Cauliflower Florets", "Maida (All-Purpose Flour)", "Cornflour", "Ginger-Garlic Paste", "Soy Sauce", "Tomato Ketchup", "Red Chili Sauce", "Green Chilies", "Spring Onion", "Capsicum", "Salt", "Black Pepper", "Oil", "Water"],
    instructions="Gobi Manchurian is a popular Indo-Chinese appetizer. Start by blanching cauliflower florets in hot water. Prepare a batter using maida, cornflour, salt, pepper, and water. Dip the florets in the batter and deep-fry until crispy. In a separate pan, sauté chopped garlic, ginger, green chilies, and spring onions in oil. Add capsicum and stir-fry briefly. Mix in soy sauce, tomato ketchup, red chili sauce, and a splash of water. Add the fried cauliflower and toss well until evenly coated. Garnish with spring onion greens and serve hot.",
    image_url = "static/images/gobi_manchurian.jpeg",
    type="veg",
    cuisine="Chinese"
    ),

    Recipe(
    id=9,
    title="Butter Chicken",
    ingredients=["Chicken", "Butter", "Tomatoes", "Cream", "Ginger-Garlic Paste", "Red Chili Powder", "Garam Masala", "Kasuri Methi", "Salt", "Oil", "Onions", "Coriander Leaves"],
    instructions="Butter Chicken is a creamy, mildly spiced chicken curry. Marinate chicken with yogurt and spices, then grill or pan-fry. Prepare a tomato-based gravy with butter, onions, ginger-garlic paste, and cream. Add the cooked chicken pieces, kasuri methi, and simmer until flavors meld. Garnish with coriander and serve with naan or rice.",
    image_url="static/images/butter_chicken.jpeg",
    type="non-veg",
    cuisine="North"
),

Recipe(
    id=10,
    title="Chicken Biriyani",
    ingredients=["Basmati Rice", "Chicken", "Yogurt", "Onions", "Tomatoes", "Ginger-Garlic Paste", "Biryani Masala", "Mint Leaves", "Coriander Leaves", "Green Chilies", "Saffron", "Milk", "Salt", "Oil", "Ghee"],
    instructions="Chicken Biryani is a fragrant layered rice dish. Marinate chicken with yogurt and spices, then cook partially. Parboil basmati rice. Layer chicken and rice, sprinkle saffron milk, and cook on low heat (dum) until done. Serve hot with raita or salan.",
    image_url="static/images/chicken_biriyani.jpeg",
    type="non-veg",
    cuisine="South"
),

Recipe(
    id=11,
    title="Fish Curry",
    ingredients=["Fish Fillets", "Tamarind Pulp", "Onions", "Tomatoes", "Mustard Seeds", "Fenugreek Seeds", "Curry Leaves", "Red Chili Powder", "Turmeric Powder", "Coriander Powder", "Garlic", "Salt", "Oil", "Coconut Milk"],
    instructions="Fish Curry is a tangy and spicy coastal dish. Prepare a tamarind-based gravy with spices, onions, and tomatoes. Add fish fillets and cook gently until tender. Finish with coconut milk for richness. Serve with steamed rice.",
    image_url="static/images/fish_curry.jpeg",
    type="non-veg",
    cuisine="South"
),

Recipe(
    id=12,
    title="Mutton Rogan Josh",
    ingredients=["Mutton", "Yogurt", "Onions", "Garlic", "Ginger", "Tomatoes", "Red Chili Powder", "Garam Masala", "Fennel Seeds", "Cloves", "Cinnamon", "Cardamom", "Salt", "Oil"],
    instructions="Mutton Rogan Josh is a rich and aromatic curry. Brown the mutton pieces, then cook with a blend of spices, yogurt, and onions until tender. The dish is known for its deep red color and intense flavors. Serve with steamed rice or naan.",
    image_url="static/images/mutton_rogan_josh.jpeg",
    type="non-veg",
    cuisine="North"
),

Recipe(
    id=13,
    title="Chicken Chettinad",
    ingredients=["Chicken", "Coconut", "Dry Red Chilies", "Black Peppercorns", "Fennel Seeds", "Coriander Seeds", "Cumin Seeds", "Cinnamon", "Cloves", "Onions", "Tomatoes", "Ginger-Garlic Paste", "Curry Leaves", "Oil", "Salt"],
    instructions="Chicken Chettinad is a spicy and flavorful South Indian curry. Grind freshly roasted spices with coconut to make a masala paste. Cook chicken with onions, tomatoes, and the masala paste until tender. Garnish with curry leaves and serve with rice or dosa.",
    image_url="static/images/chicken_chettinad.jpeg",
    type="non-veg",
    cuisine="South"
),

Recipe(
    id=14,
    title="Prawn Masala",
    ingredients=["Prawns", "Onions", "Tomatoes", "Ginger-Garlic Paste", "Red Chili Powder", "Turmeric Powder", "Garam Masala", "Coriander Powder", "Curry Leaves", "Oil", "Salt", "Coriander Leaves"],
    instructions="Prawn Masala is a spicy coastal dish with juicy prawns cooked in a rich onion-tomato gravy. Sauté onions and ginger-garlic paste, add spices and tomatoes, then cook prawns until done. Garnish with coriander leaves and serve hot with rice or roti.",
    image_url="static/images/prawn_masala.jpeg",
    type="non-veg",
    cuisine="South"
),

Recipe(
    id=15,
    title="Egg Curry",
    ingredients=["Boiled Eggs", "Onions", "Tomatoes", "Ginger-Garlic Paste", "Red Chili Powder", "Turmeric Powder", "Garam Masala", "Coriander Powder", "Oil", "Salt", "Coriander Leaves"],
    instructions="Egg Curry features boiled eggs simmered in a spicy onion-tomato gravy. Fry onions and ginger-garlic paste, add spices and tomatoes, then add boiled eggs and cook for a few minutes. Garnish with coriander leaves and serve with rice or chapati.",
    image_url="static/images/egg_curry.jpeg",
    type="non-veg",
    cuisine="North"
),

Recipe(
    id=16,
    title="Chicken 65",
    ingredients=["Chicken", "Yogurt", "Ginger-Garlic Paste", "Red Chili Powder", "Turmeric Powder", "Curry Leaves", "Green Chilies", "Cornflour", "All-Purpose Flour", "Salt", "Oil", "Lemon Juice"],
    instructions="Chicken 65 is a popular spicy fried chicken snack. Marinate chicken pieces with yogurt, spices, and flours. Deep fry until crispy and golden. Toss with fried curry leaves, green chilies, and a splash of lemon juice. Serve hot as an appetizer or snack.",
    image_url="static/images/chicken_65.jpeg",
    type="non-veg",
    cuisine="South"
),
Recipe(
    id=17,
    title="Dragon Chicken",
    ingredients=["Boneless Chicken", "Cornflour", "All-Purpose Flour", "Ginger-Garlic Paste", "Soy Sauce", "Tomato Ketchup", "Red Chili Sauce", "Green Chilies", "Capsicum", "Spring Onion", "Garlic", "Salt", "Pepper", "Oil", "Sugar", "Vinegar"],
    instructions="Dragon Chicken is a spicy Indo-Chinese chicken dish that's crispy, tangy, and sweet. Start by marinating thinly sliced boneless chicken with ginger-garlic paste, soy sauce, salt, pepper, cornflour, and all-purpose flour. Deep fry until golden and crispy. In a wok, heat oil and sauté chopped garlic, green chilies, and sliced onions. Add sliced capsicum and cook briefly. Stir in tomato ketchup, red chili sauce, soy sauce, sugar, and vinegar to make the dragon sauce. Toss in the fried chicken and mix until the sauce coats evenly. Garnish with spring onion greens and serve hot as a starter or side.",
    image_url="static/images/dragon_chicken.jpeg",
    type="non-veg",
    cuisine="Chinese"
),
Recipe(
    id=18,
    title="Schezwan Noodles",
    ingredients=["Noodles", "Schezwan Sauce", "Garlic", "Ginger", "Green Chilies", "Onion", "Capsicum", "Carrot", "Cabbage", "Soy Sauce", "Vinegar", "Salt", "Pepper", "Oil", "Spring Onion"],
    instructions="Schezwan Noodles are spicy Indo-Chinese stir-fried noodles with bold flavors. Boil noodles until al dente, rinse with cold water, and toss with a little oil to prevent sticking. In a wok, heat oil and sauté chopped garlic, ginger, and green chilies. Add sliced onions, capsicum, carrot, and cabbage; stir-fry on high flame until slightly tender. Add boiled noodles and toss in Schezwan sauce, soy sauce, vinegar, salt, and pepper. Stir-fry for 2-3 minutes until everything is well mixed. Garnish with chopped spring onions and serve hot.",
    image_url="static/images/schezwan_noodles.jpeg",
    type="veg",
    cuisine="Chinese"
),
Recipe(
    id=19,
    title="Veg Chow Mein",
    ingredients=["Noodles", "Garlic", "Ginger", "Green Chilies", "Onion", "Capsicum", "Cabbage", "Carrot", "Soy Sauce", "Vinegar", "Green Chili Sauce", "Salt", "Pepper", "Oil", "Spring Onion"],
    instructions="Chow Mein is a flavorful Chinese-style stir-fried noodle dish. Cook noodles as per instructions, drain, and set aside. Heat oil in a wok and sauté minced garlic, ginger, and green chilies. Add julienned onions, capsicum, carrots, and cabbage. Stir-fry on high flame till veggies are slightly tender but still crunchy. Add cooked noodles along with soy sauce, vinegar, green chili sauce, salt, and pepper. Toss everything well and stir-fry for a few more minutes. Garnish with spring onion greens and serve hot.",
    image_url="static/images/chow_mein.jpeg",
    type="veg",
    cuisine="Chinese"
),
Recipe(
    id=20,
    title="Spring Rolls",
    ingredients=["Spring Roll Sheets", "Cabbage", "Carrot", "Capsicum", "Beans", "Garlic", "Soy Sauce", "Vinegar", "Salt", "Pepper", "Cornflour", "Oil"],
    instructions="Spring Rolls are crispy deep-fried snacks filled with spiced vegetables. Finely shred cabbage, carrots, capsicum, and beans. In a pan, heat oil and sauté chopped garlic, then add veggies and stir-fry on high heat. Add soy sauce, vinegar, salt, and pepper. Cool the filling. Take spring roll sheets, place a spoonful of filling, fold and seal the edges with cornflour paste. Deep-fry the rolls until golden and crispy. Serve hot with chili sauce or ketchup.",
    image_url="static/images/spring_rolls.jpeg",
    type="veg",
    cuisine="Chinese"
),


]

@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    q: Optional[str] = None,
    filter_type: Optional[str] = None,
    cuisine: Optional[str] = None
):
    filtered = recipes

    if q:
        filtered = [r for r in filtered if q.lower() in r.title.lower()]
    if filter_type in ["veg", "non-veg"]:
        filtered = [r for r in filtered if r.type == filter_type]
    if cuisine:
        filtered = [r for r in filtered if r.cuisine.lower() == cuisine.lower()]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "recipes": filtered,
        "filter_type": filter_type,
        "cuisine": cuisine
    })

@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def read_recipe(request: Request, recipe_id: int):
    recipe = next((r for r in recipes if r.id == recipe_id), None)
    if recipe is None:
        return HTMLResponse(content="Recipe not found", status_code=404)
    return templates.TemplateResponse("recipe.html", {"request": request, "recipe": recipe})


