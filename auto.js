const autoLike = async () => {
    const likeButton = document.querySelector('div[role=button]:has(svg[aria-label="Like"])');
    if (likeButton) {
        likeButton.click();
    }
    return "liked";
}

const autoComment = async () => {

    const randomPositiveCompliments = [
        // heart eyes
        "😍😍😍 wowowow",
        // black hearts
        "🖤🖤🖤 yesss",
        // fire
        "🔥🔥🔥 duuuude",
        // 100
        "💯💯💯 woah",
        // heart
        "❤️❤️❤️ woah",
        // wow emoji
        "😲😲😲 dude",
        // star eyes
        "🤩🤩🤩 wowowow",
        // stars
        "⭐⭐⭐ yessss!",
        "😲😲😲 omg",
    ]
    const randomCompliment = randomPositiveCompliments[Math.floor(Math.random() * randomPositiveCompliments.length)];

    let commentTextArea = document.querySelector('textarea');
    // submit button is div[role=button] with text "Post"
    let submitButton = Array.from(document.querySelectorAll('div[role=button]')).filter((el) => el.innerText === 'Post')[0];


    // if the comment textarea and submit button are found, fill in the comment and submit it
    if (commentTextArea && submitButton) {
        commentTextArea.click();
        commentTextArea.focus();
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
        nativeInputValueSetter.call(commentTextArea, randomCompliment);
        setTimeout(() => {
            const ev = new Event('input', { bubbles: true });
            commentTextArea.dispatchEvent(ev);
        }, 500);
        setTimeout(() => {
            submitButton.click();
        }, 1500);

        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve("commented")
            }, 2500);
        });
    } else {
        return new Promise((resolve, reject) => {
            resolve("no comment box found")
        });
    }


}

function autoLikeAndComment(nSecondDelay) {
    /*
args: nSecondDelay (seconds)

repeat indefinitely. 
0. wait nSecondDelay seconds
1. click body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div:nth-child(1) > div > div > div._aaqg._aaqh > button
2. wait nSecondDelay seconds
2. click body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x1qjc9v5.xjbqb8w.x1lcm9me.x1yr5g0i.xrt01vj.x10y3i5r.xr1yuqi.xkrivgy.x4ii5y1.x1gryazu.x15h9jz8.x47corl.xh8yej3.xir0mxb.x1juhsu6 > div > article > div > div.x1qjc9v5.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x5wqa0o.xln7xf2.xk390pu.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x65f84u.x1vq45kp.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x11njtxf > div > div > div.x78zum5.xdt5ytf.x1q2y9iw.x1n2onr6.xh8yej3.x9f619.x1iyjqo2.x18l3tf1.x26u7qi.xy80clv.xexx8yu.x4uap5.x18d9i69.xkhd6sd > section.x78zum5.x1q0g3np.xwib8y2.x1yrsyyn.x1xp8e9x.x13fuv20.x178xt8z.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xo1ph6p.x1pi30zi.x1swvt13 > span.x1rg5ohu.xp7jhwk > div > div
*/
    //next button selector: button that contains an svg[aria-label="Next"]
    const nextButton = document.querySelector('button:has(svg[aria-label="Next"])');
    if (nextButton) {
        nextButton.click();
    }

    setTimeout(() => {
        autoLike().then((res) => {
            if (res === "liked") {
                autoComment().then((commentRes) => {
                    if (commentRes === "commented" || commentRes === "no comment box found") {
                        setTimeout(() => {
                            autoLikeAndComment(nSecondDelay);
                        }, nSecondDelay * 1000);
                    }
                })
            }
        });
    }, nSecondDelay * 1000);
}

autoLikeAndComment(1);
