const SpriteManager = (() => {

    const BASE_PATH = "chars/";

    function getFolder(isAlien) {
        return isAlien ? "alien/" : "human/";
    }

    function getSprite(passenger, expression = "def") {
        const folder = getFolder(passenger.true_species === 0);
        const id = passenger.id;
        const path = `${BASE_PATH}${folder}${id}/${id}_${expression}.png`;
        console.log(`[Sprite] Loading main sprite: ${path}`);
        return path;
    }

    function getPassportSprite(passengerId, isAlien) {
        const folder = getFolder(isAlien);
        const path = `${BASE_PATH}${folder}${passengerId}/${passengerId}_passport.png`;
        console.log(`[Passport] Trying to load: ${path}`);
        return path;
    }

    function getFallback(expression = "def") {
        const path = `${BASE_PATH}default/def_${expression}.png`;
        console.log(`[Fallback] Using: ${path}`);
        return path;
    }

    function loadSprite(imgElement, path, fallback) {
        console.log(`[Load] Attempting to load: ${path}`);
        imgElement.src = path;

        imgElement.onerror = () => {
            console.error(`[ERROR] Failed to load: ${path} → falling back`);
            imgElement.src = fallback;
        };
    }

    return {
        getSprite,
        getPassportSprite,
        getFallback,
        loadSprite,
        renderPassenger
    };

})();
