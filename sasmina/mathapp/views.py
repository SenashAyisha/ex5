from django.shortcuts import render

def powercalc(request):
    context = {
        'power': '',
        'v': '',
        'i': '',
        'r': '',
        'error': ''
    }

    if request.method == "POST":
        # Read and normalize inputs
        v = (request.POST.get('voltage', '') or '').strip()
        i = (request.POST.get('current', '') or '').strip()
        r = (request.POST.get('resistance', '') or '').strip()

        # Replace comma with dot if user typed "230,0"
        v = v.replace(',', '.') if v else v
        i = i.replace(',', '.') if i else i
        r = r.replace(',', '.') if r else r

        context['v'], context['i'], context['r'] = v, i, r

        # Try converting inputs to floats when provided
        try:
            V = float(v) if v != '' else None
            I = float(i) if i != '' else None
            R = float(r) if r != '' else None
        except ValueError:
            context['error'] = "Please enter valid numeric values (use digits, e.g. 230 or 0.26)."
            return render(request, "mathapp/mathapp.html", context)

        # Require at least two values
        provided_count = sum(x is not None for x in (V, I, R))
        if provided_count < 2:
            context['error'] = "Please provide at least two values (Voltage, Current or Resistance)."
            return render(request, "mathapp/mathapp.html", context)

        # Compute power by available formulas (prefer V*I if available)
        try:
            if V is not None and I is not None:
                power = V * I
            elif I is not None and R is not None:
                power = I * I * R
            elif V is not None and R is not None:
                if R == 0:
                    context['error'] = "Resistance cannot be zero."
                    return render(request, "mathapp/mathapp.html", context)
                power = (V * V) / R
            else:
                context['error'] = "Unexpected input combination."
                return render(request, "mathapp/mathapp.html", context)

            # Round result for display
            context['power'] = round(power, 4)
        except Exception as e:
            context['error'] = f"Computation error: {e}"

    return render(request, "mathapp/mathapp.html", context)




