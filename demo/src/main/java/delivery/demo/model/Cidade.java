package delivery.demo.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import lombok.*;

import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString(exclude = {"fretes"})
@Table(name = "cidade")
public class Cidade {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Nome dad cidade é obrigatório")
    private String nome;

    @NotBlank(message = "UF é obrigatório")
    @Size(min = 2, max = 2, message = "UF deve ter 2 caracteres")
    private String uf;

    @NotNull(message = "O valor da taxa de entrega é obrigatório")
    @Positive(message = "O valor da taxa deve ser positivo")
    private Double taxa;

    @OneToMany(mappedBy = "cidade")
    private List<Frete> fretes;

    public Cidade(String nome, String uf, Double taxa) {
        this.nome = nome;
        this.uf = uf;
        this.taxa = taxa;
    }
}

