var toggle = false;
function myfunc()
{
    if (window.matchMedia("(max-width : 952px)"))
    toggle = !toggle

    window.setTimeout(function()
    {
        var item = document.querySelectorAll(".navbar_container > .nav_item a");

        for (var i = 0 ; i < item.length ; i++)
        {
            if (toggle)
            {
                item[i].style.display = "block";
            }
            
            else
            {
                item[i].style.display = "none";
            }
        }
        document.querySelector(".navbar_container > .nav_item > .hamburger").style.display = "block";
    }, 100);

}